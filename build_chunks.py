#!/usr/bin/env python3
"""
Wandelt Folien-JSONs (eine Datei pro Vorlesung, Liste von Folien) in Chunks um.

Aufruf:
    python build_chunks.py Ausgabe [-o chunks.jsonl] [--pattern slides.json] [--no-raw] [--preview 3]

Zusätzlich entsteht pro Vorlesung eine kompakte Kapitel-Datei (Ordner "kapitel/")
für den LLM-Kontext (Small-to-Big), plus kapitel/index.json mit Token-Schätzung.

Ergebnis: chunks.jsonl mit einer Zeile pro Chunk:
    {"id": ..., "kind": "folie" | "gliederung", "text": ..., "metadata": {...}}

"text" wird eingebettet und für BM25 indiziert. "metadata" wird nur gespeichert
(Filter, Quellenangabe, Bild anzeigen), nicht eingebettet.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------- Einstellungen

# Zeilen, die komplett entfernt werden (Fußzeilen, Seitenzahlen). Bei Bedarf erweitern.
FOOTER_PATTERNS = [
    re.compile(r"^Prof\.\s*Dr\..*\d{1,2}\.\d{1,2}\.\d{4}\s*$"),  # Prof. Dr. ... 09.04.2025
    re.compile(r"^\|\s*\d*$"),                                    # "|     4" oder nur "|"
    re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}\s*\|\s*\d+$"),         # "09.04.2025 | 19"
    re.compile(r"^[\d.*\s]+$"),                                   # "1 1", "0..1 *" (Multiplizitäten aus Diagrammen)
]

# Betonungs-Hinweise der Bildbeschreibung, die als Text nichts sagen
EMPHASIS_PATTERNS = [
    # "(betont)", "(beide Begriffe betont)", "(betont: "wichtig")", "(wobei "X" betont ist)"
    re.compile(r"\s*\((?:[^()]*\s)?betont(?:\s+(?:ist|sind))?(?::[^()]*)?\)"),
    # übrig gebliebene Halbsätze: ", wobei der Teil „X" ist." / ", wobei „X" ist."
    re.compile(r",?\s*wobei der Teil\s+„[^„]*?[\"“”]\s+ist(?=[.\s])"),
    re.compile(r",?\s*wobei\s+„[^„]*?[\"“”]\s+ist(?=\.)"),
    re.compile(r"\s*Dabei sind die Wörter[^.]*\."),
]

# Abbildungsbeschreibung auch ohne erkanntes Diagramm behalten? (False = Deko/Comic/Foto verwerfen)
KEEP_ABBILDUNG_WITHOUT_DIAGRAM = False

# Mindestanzahl Folien mit identischer BEGRIFFE-Liste, ab der sie als Wiederholung gelten
REPEATED_TERMS_MIN = 3

# Kapitel-Dateien
CHARS_PER_TOKEN = 3.0          # grobe Schätzung für deutschen Text (eher vorsichtig)
DEFAULT_MAX_DIAGRAM_CHARS = 1200   # Abbildungsbeschreibungen im Kapitelkontext kürzen
URL_RE = re.compile(r"https?://\S+")

SECTION_RE = re.compile(r"^(THEMA|INHALT|FORMELN|ABBILDUNGEN|BEGRIFFE):[ \t]*", re.M)

# Folien, die kaum Inhalt tragen (werden markiert, nicht gelöscht)
LOW_VALUE_RE = re.compile(
    r"Gliederungsfolie|Übersichtsfolie|Titelfolie|Titel- und|Agenda|Inhaltsverzeichnis", re.I
)
DECORATIVE_RE = re.compile(r"dekorativ|ohne technische information", re.I)


# ---------------------------------------------------------------- Bereinigung

def clean_raw_text(text: str, title: str) -> str:
    """Fußzeile, Seitenzahl, URLs und Layout-Leerraum aus dem Rohtext entfernen."""
    lines = []
    for line in (text or "").splitlines():
        line = URL_RE.sub("", line)
        line = re.sub(r"[ \t]{2,}", " ", line).strip()
        if any(p.match(line) for p in FOOTER_PATTERNS):
            continue
        lines.append(line)

    # Titel steht schon im Header -> erste Zeile weg, falls identisch
    while lines and not lines[0]:
        lines.pop(0)
    if lines and lines[0].strip() == (title or "").strip():
        lines.pop(0)

    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return out


def parse_description(desc: str) -> dict:
    """Beschreibung in ihre Abschnitte (THEMA, INHALT, ...) zerlegen."""
    parts = {}
    matches = list(SECTION_RE.finditer(desc or ""))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(desc)
        parts[m.group(1)] = desc[m.end():end].strip()
    return parts


def clean_section(value: str) -> str:
    # Formatierungs-Rauschen: "(betont)", "(beide Begriffe betont)", ...
    for pat in EMPHASIS_PATTERNS:
        value = pat.sub("", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def is_empty_section(value: str) -> bool:
    v = value.strip().lower().rstrip(".")
    return v == "" or v in {"-", "–"} or (v.startswith("keine") and len(v) < 40)


# ---------------------------------------------------------------- Chunk-Bau

def build_slide_chunk(slide: dict, include_raw: bool) -> dict:
    lecture = slide.get("lecture", "UNBEKANNT")
    nr = slide.get("slide")
    title = (slide.get("title") or "").strip()
    desc_parts = parse_description(slide.get("description", ""))
    diagrams = slide.get("diagram_classes") or []

    # Abbildungsbeschreibung nur behalten, wenn sie Information trägt
    abb = clean_section(desc_parts.get("ABBILDUNGEN", ""))
    has_readable_diagram = any(d.get("lesbar") for d in diagrams)
    if is_empty_section(abb):
        abb = ""
    elif DECORATIVE_RE.search(abb):
        abb = ""
    elif diagrams and not has_readable_diagram:
        abb = ""  # Diagramm nicht lesbar -> Beschreibung unzuverlässig
    elif not diagrams and not KEEP_ABBILDUNG_WITHOUT_DIAGRAM:
        abb = ""  # kein Diagramm erkannt -> Illustration/Comic/Foto

    sections = [
        ("Thema", clean_section(desc_parts.get("THEMA", ""))),
        ("Inhalt", clean_section(desc_parts.get("INHALT", ""))),
        ("Formeln", clean_section(desc_parts.get("FORMELN", ""))),
        ("Abbildung", abb),
        ("Begriffe", clean_section(desc_parts.get("BEGRIFFE", ""))),
    ]
    sections = [(k, v) for k, v in sections if v and not is_empty_section(v)]

    context_sections = list(sections)  # ohne Rohtext, für die Kapitel-Datei
    raw = clean_raw_text(slide.get("text", ""), title)
    if include_raw and raw:
        sections.append(("Originaltext", raw))

    header = f"Vorlesung: {lecture} | Folie {nr} | Titel: {title}"
    body = "\n".join(f"{k}: {v}" for k, v in sections)
    text = f"{header}\n{body}".strip()

    thema = desc_parts.get("THEMA", "")
    metadata = {
        "lecture": lecture,
        "slide": nr,
        "title": title,
        "image": slide.get("image", ""),
        "has_diagram": has_readable_diagram,
        "diagram_arts": ",".join(d.get("art", "") for d in diagrams),
        "low_value": bool(LOW_VALUE_RE.search(thema)),
    }
    begriffe = frozenset(
        t.strip().lower().rstrip(".")
        for t in clean_section(desc_parts.get("BEGRIFFE", "")).split(",") if t.strip()
    )
    return {
        "_begriffe": begriffe,  # nur intern, wird vor dem Schreiben entfernt
        "_sections": context_sections,  # nur intern
        "id": f"{lecture}#{int(nr):03d}",
        "kind": "folie",
        "text": text,
        "metadata": metadata,
    }


def build_outline_chunk(lecture: str, slides: list) -> dict:
    lines = [f"Gliederung der Vorlesung {lecture} ({len(slides)} Folien)"]
    for s in slides:
        lines.append(f"Folie {s['slide']}: {(s.get('title') or '').strip()}")
    return {
        "id": f"{lecture}#gliederung",
        "kind": "gliederung",
        "text": "\n".join(lines),
        "metadata": {
            "lecture": lecture,
            "slide": 0,
            "title": "Gliederung",
            "image": "",
            "has_diagram": False,
            "diagram_arts": "",
            "low_value": False,
        },
    }


# ---------------------------------------------------------------- Kapitel-Dateien

def shorten(text: str, limit: int) -> str:
    """Text an einer Wortgrenze kürzen (limit 0 = nicht kürzen)."""
    if not limit or len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " … [gekürzt]"


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip()


def build_chapter_text(lecture: str, lec_chunks: list, max_diagram_chars: int) -> str:
    """Kompakter Kontext-Text einer Vorlesung: ohne Rohtext und Begriffe-Liste."""
    slides = [c for c in lec_chunks if c["kind"] == "folie"]
    parts = [f"# {lecture} ({len(slides)} Folien)"]
    for c in slides:
        m = c["metadata"]
        head = f"## Folie {m['slide']}: {m['title']}"
        if m["low_value"]:
            parts.append(head + "\n(Titel-/Gliederungsfolie ohne weiteren Inhalt)")
            continue
        lines = []
        for key, val in c["_sections"]:
            if key == "Begriffe":
                continue
            if key == "Abbildung":
                val = shorten(val, max_diagram_chars)
            lines.append(f"{key}: {val}")
        parts.append(head + "\n" + "\n".join(lines))
    return "\n\n".join(parts) + "\n"


def estimate_tokens(text: str) -> int:
    return round(len(text) / CHARS_PER_TOKEN)


# ---------------------------------------------------------------- Hauptprogramm

def natural_key(text: str):
    """'Kapitel 10' soll nach 'Kapitel 2' kommen."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text)]


def load_slides(folder: Path, pattern: str) -> list:
    slides = []
    files = sorted(folder.rglob(pattern), key=lambda p: natural_key(str(p)))
    if not files:
        sys.exit(f"Keine Dateien '{pattern}' in {folder} gefunden.")
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"WARNUNG: {f} ist kein gültiges JSON ({e}), übersprungen.")
            continue
        if isinstance(data, dict):
            data = [data]
        for s in data:
            s["_source_file"] = str(f)
            slides.append(s)
    return slides


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=Path("chunks.jsonl"))
    ap.add_argument("--pattern", default="slides.json",
                    help="Dateiname der Folien-JSONs (Standard: slides.json)")
    ap.add_argument("--chapters-dir", type=Path, default=Path("kapitel"),
                    help="Zielordner für die Kapitel-Dateien (Standard: kapitel)")
    ap.add_argument("--no-chapters", action="store_true",
                    help="Keine Kapitel-Dateien erzeugen")
    ap.add_argument("--max-diagram-chars", type=int, default=DEFAULT_MAX_DIAGRAM_CHARS,
                    help="Abbildungsbeschreibungen im Kapitelkontext auf so viele "
                         "Zeichen kürzen (0 = nicht kürzen)")
    ap.add_argument("--budget-tokens", type=int, default=30000,
                    help="Warnung, wenn ein Kapitel diese Token-Schätzung überschreitet")
    ap.add_argument("--no-raw", action="store_true",
                    help="Rohtext nicht in den Chunk-Text aufnehmen")
    ap.add_argument("--preview", type=int, default=0,
                    help="So viele Chunks zur Kontrolle auf der Konsole ausgeben")
    args = ap.parse_args()

    slides = load_slides(args.input_dir, args.pattern)
    by_lecture = defaultdict(list)
    for s in slides:
        by_lecture[s.get("lecture", "UNBEKANNT")].append(s)

    chunks, warnings, seen = [], [], set()
    chapter_info = []
    if not args.no_chapters:
        args.chapters_dir.mkdir(parents=True, exist_ok=True)
    for lecture, lec_slides in sorted(by_lecture.items(), key=lambda kv: natural_key(kv[0])):
        lec_slides.sort(key=lambda s: s.get("slide", 0))
        lec_chunks = []
        for s in lec_slides:
            chunk = build_slide_chunk(s, include_raw=not args.no_raw)
            if chunk["id"] in seen:
                warnings.append(f"Doppelte ID: {chunk['id']}")
                continue
            seen.add(chunk["id"])
            if not (s.get("description") or "").strip():
                warnings.append(f"{chunk['id']}: keine Beschreibung (nur Rohtext)")
            if len(chunk["text"].splitlines()) <= 1:
                warnings.append(f"{chunk['id']}: Chunk praktisch leer")
            lec_chunks.append(chunk)

        # Folien mit identischer Begriffe-Liste (wiederkehrende Gliederungsfolien) abwerten
        counts = Counter(c["_begriffe"] for c in lec_chunks if c["_begriffe"])
        for c in lec_chunks:
            if c["_begriffe"] and counts[c["_begriffe"]] >= REPEATED_TERMS_MIN:
                c["metadata"]["low_value"] = True

        if not args.no_chapters:
            text = build_chapter_text(lecture, lec_chunks, args.max_diagram_chars)
            fname = safe_filename(lecture) + ".md"
            (args.chapters_dir / fname).write_text(text, encoding="utf-8")
            chapter_info.append({
                "lecture": lecture,
                "file": str(args.chapters_dir / fname),
                "slides": sum(1 for c in lec_chunks if c["kind"] == "folie"),
                "chars": len(text),
                "tokens_est": estimate_tokens(text),
            })

        for c in lec_chunks:
            c.pop("_begriffe")
            c.pop("_sections")

        chunks.extend(lec_chunks)
        chunks.append(build_outline_chunk(lecture, lec_slides))

    with args.output.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    n_slides = sum(1 for c in chunks if c["kind"] == "folie")
    n_low = sum(1 for c in chunks if c["metadata"]["low_value"])
    lengths = [len(c["text"]) for c in chunks if c["kind"] == "folie"]
    print(f"{len(by_lecture)} Vorlesungen, {n_slides} Folien-Chunks, "
          f"{len(by_lecture)} Gliederungs-Chunks -> {args.output}")
    if lengths:
        print(f"Chunk-Länge (Zeichen): min {min(lengths)}, "
              f"Ø {sum(lengths) // len(lengths)}, max {max(lengths)}")
    print(f"Als 'low_value' markiert: {n_low}")
    for w in warnings:
        print("WARNUNG:", w)

    if chapter_info:
        (args.chapters_dir / "index.json").write_text(
            json.dumps(chapter_info, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nKapitel-Dateien in {args.chapters_dir}/ (Token = Zeichen / {CHARS_PER_TOKEN:g}, grobe Schätzung):")
        for ci in chapter_info:
            flag = "  <-- über Budget" if ci["tokens_est"] > args.budget_tokens else ""
            print(f"  {ci['tokens_est']:>7,} Token  {ci['slides']:>3} Folien  {ci['lecture']}{flag}")
        total = sum(ci["tokens_est"] for ci in chapter_info)
        biggest = sorted((ci["tokens_est"] for ci in chapter_info), reverse=True)[:2]
        print(f"  {total:>7,} Token  Summe aller Kapitel")
        if len(biggest) == 2:
            print(f"  Die zwei größten Kapitel zusammen: {sum(biggest):,} Token")

    for c in chunks[: args.preview]:
        print("\n" + "=" * 70)
        print(c["id"], c["metadata"])
        print("-" * 70)
        print(c["text"])


if __name__ == "__main__":
    main()
