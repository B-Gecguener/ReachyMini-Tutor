"""
Lässt Qwen (über Ollama) jede Folie beschreiben und speichert die Beschreibung
in der slides.json, die render_slides.py erzeugt hat.

Installation:  pip install requests python-dotenv

Einstellungen in einer Datei .env im selben Ordner wie dieses Skript:
    OPENWEBUI_API_KEY=sk-...
    OLLAMA_HOST=http://localhost:3000/ollama
    OLLAMA_MODEL=qwen3.8:27b
    OLLAMA_CLASSIFY_MODEL=         (optional: kleineres Modell für die Klassifikation)

Dann reicht:
    python describe_slides.py ausgabe/ --limit 3

Kommandozeilen-Optionen (--api-key, --host, --model, --classify-model) haben
Vorrang vor der .env. Ohne Open WebUI: OLLAMA_HOST=http://localhost:11434 und keinen Key.

Ablauf pro Folie:
1. Klassifikation (kurzer Aufruf, ohne Thinking): Welche Diagramme sind zu sehen,
   welche Art, sind sie lesbar, und sind sie Gegenstand der Folie oder nur ein
   Beispielbild? Das Ergebnis steht in der slides.json (diagram_classes).
2. Beschreibung: Der Prompt enthält nur die Regeln der Diagrammarten, die auf dieser
   Folie Gegenstand sind. Beispielbilder werden nur in ein bis zwei Sätzen erwähnt.

Manuelle Korrekturen in der slides.json (bleiben bei render_slides.py erhalten):
    "hint": "Freitext für das Modell"      Hinweis des Autors zu dieser Folie
    "diagrams": []                         alle Diagramme nur als Beispielbild
    "diagrams": ["sequenz"]                diese Arten vollständig beschreiben
    (erlaubte Arten: klasse, sequenz, aktivitaet, zustand, andere)
Mit "diagrams" wird die automatische Klassifikation für diese Folie übersprungen.
Um eine Folie neu klassifizieren zu lassen, "diagram_classes" aus der Folie löschen.

- Fortsetzbar: Bereits beschriebene Folien werden übersprungen. Abbrechen mit
  Strg+C und später neu starten ist kein Problem.
- Nach jeder Folie wird gespeichert.
- Die Prompt-Version wird pro Folie berechnet (Kernprompt + benutzte Diagramm-Regeln).
  Ändert sich eine Regel, werden nur die Folien neu beschrieben, die sie benutzen.
  Ändert sich der Kernprompt, werden alle Folien neu beschrieben.
- Ändert sich der Hint einer Folie, wird sie neu beschrieben.
- --redo erzwingt eine neue Beschreibung, auch bei aktuellem Prompt
  (nicht fortsetzbar: nach einem Abbruch beginnt es wieder vorne).
"""

import argparse
import base64
import difflib
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# .env neben dem Skript laden, egal aus welchem Ordner es gestartet wird.
# Bereits gesetzte Umgebungsvariablen werden nicht überschrieben.
load_dotenv(Path(__file__).resolve().with_name(".env"))

# ---------------------------------------------------------------------------
# Kernprompt (gilt für jede Folie)
# ---------------------------------------------------------------------------

PROMPT = """Du bekommst eine Folie aus der Vorlesung "{lecture}" (Folie {slide}).
Vorherige Folie: "{prev_title}".
{context}
{hint}
Extrahierter Text der Folie (kann unvollständig oder durcheinander sein):
---
{text}
---

Beschreibe den INHALT der Folie auf Deutsch so, dass jemand ihn ohne das Bild
vollständig versteht. Die Beschreibung dient später als Wissensbasis für einen Tutor.
Gliedere die Antwort genau so:

THEMA: Ein Satz, worum es auf der Folie geht.
INHALT: Die Aussagen der Folie in ganzen Sätzen, in der Reihenfolge der Folie.
FORMELN: Jede Formel in LaTeX und zusätzlich ausgesprochen (z. B. "x hoch zwei"). Sonst "keine".
ABBILDUNGEN: Diagramme, Tabellen und Grafiken (Regeln unten). Sonst "keine".
BEGRIFFE: Die wichtigsten Fachbegriffe, kommagetrennt.

Weglassen, weil es für das Verständnis nichts beiträgt:
- Logos, Hochschul-Branding, Hintergrund- und Zierelemente, Farben und Layout.
- Die Fußzeile (Kursname, Datum, Foliennummer).
- Schrift- und Farbhervorhebungen. Ist etwas erkennbar betont, schreib nur "(betont)" dahinter.

Diagramme und Tabellen:
- Jede Information nur einmal: Steht etwas unter ABBILDUNGEN, wiederhole es nicht unter INHALT.
- Tabellen: Zeile für Zeile wiedergeben.
{diagram_info}

Allgemein:
- Beschreibe nur, was auf der Folie steht oder zu sehen ist. Erfinde nichts dazu
  und deute nichts hinein.
- Titel-, Gliederungs- und Organisationsfolien: Unter THEMA die Art der Folie nennen,
  unter INHALT höchstens drei Sätze.
- Unleserliches markierst du mit [unleserlich] (nur für einzelne Wörter, nicht für
  ganze Diagramme)."""


# ---------------------------------------------------------------------------
# Bausteine pro Diagrammart (nur eingefügt, wenn das Diagramm Gegenstand der Folie ist)
# ---------------------------------------------------------------------------

DIAGRAM_RULES = {
    "klasse": """- UML-Klassen-, Objekt- und Domänenmodell-Diagramme: jede Klasse bzw. jedes Objekt
  mit Attributen (inkl. Typ und Sichtbarkeit) und Methoden; jede Beziehung mit Art
  (Assoziation, Aggregation, Komposition, Vererbung, Realisierung, Abhängigkeit),
  Richtung, Rollennamen und Multiplizitäten an beiden Enden.
  Notation genau unterscheiden: Assoziation = durchgezogene Linie (ggf. mit offenem
  Pfeil für die Navigierbarkeit). Abhängigkeit = gestrichelter Pfeil. Vererbung =
  durchgezogene Linie mit hohlem Dreieck an der Oberklasse. Realisierung = gestrichelte
  Linie mit hohlem Dreieck. Aggregation = hohle Raute, Komposition = gefüllte Raute am
  Ganzen. Ein kleines gefülltes Dreieck neben einem Beziehungsnamen zeigt nur die
  Leserichtung des Namens und ist keine Beziehungsart.""",

    "sequenz": """- Sequenzdiagramme: alle Lebenslinien, dann die Nachrichten in zeitlicher Reihenfolge
  (Sender -> Empfänger: Nachricht, synchron/asynchron/Antwort) sowie Fragmente
  (alt, opt, loop, par) mit ihren Bedingungen.""",

    "aktivitaet": """- Aktivitätsdiagramme: Start, Aktionen in Ablaufreihenfolge, Verzweigungen mit
  Bedingungen, Parallelisierung (Fork/Join), Swimlanes, Ende.
  UML-Notation genau unterscheiden:
  - Aktion: Rechteck mit abgerundeten Ecken. Objektknoten: Rechteck mit eckigen Ecken.
  - Pin: kleines Quadrat direkt an einer Aktion (Ein- oder Ausgabe).
    Aktivitätsparameterknoten: Rechteck auf dem Rand des Aktivitätsrahmens.
  - Startknoten: gefüllter schwarzer Kreis. Aktivitätsende: Kreis mit gefülltem Kern.
    Ablaufende: Kreis mit X. Entscheidung und Zusammenführung: Raute.
    Gabelung und Vereinigung (Fork/Join): dicker Balken.
  - Der abgerundete Rahmen mit dem Namen oben links ist die Aktivität selbst, keine
    Partition. Partitionen sind Bahnen (Swimlanes).
  - Farbige Punkte oder Kreise auf Kanten oder an Knoten sind meist Tokens einer
    Animation. Sie gehören nicht zum Modell: Beschreibe sie nicht als Knoten oder
    Kanten, sondern nenne unter INHALT, wo welcher Token gerade liegt.""",

    "zustand": """- Zustandsdiagramme: alle Zustände (auch Unterzustände) und jede Transition als
  Quelle -> Ziel: Ereignis [Bedingung] / Aktion.""",

    "andere": """- Andere Diagramme: Elemente, ihre Verbindungen und was man daraus ablesen soll.""",
}

EXAMPLE_RULE = (
    "Beschreibe sie unter ABBILDUNGEN zusammen in höchstens zwei Sätzen: Art des "
    "Diagramms, grobes Thema, wofür sie auf der Folie Beispiel sind. Zähle KEINE Klassen, "
    "Attribute, Beziehungen, Zustände oder Nachrichten auf, schreib keine "
    "[unleserlich]-Listen und rate nichts, was du nicht sicher lesen kannst."
)


# ---------------------------------------------------------------------------
# Klassifikation der Diagramme (Art, Lesbarkeit, Rolle)
# ---------------------------------------------------------------------------

ARTEN = list(DIAGRAM_RULES)  # klasse, sequenz, aktivitaet, zustand, andere

CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "diagramme": {
            "type": "array",
            "items": {
                "type": "object",
                # Reihenfolge ist Absicht: erst kurz beschreiben, dann festlegen
                "properties": {
                    "beschreibung": {"type": "string"},
                    "art": {"type": "string", "enum": ARTEN},
                    "lesbar": {"type": "boolean"},
                    "rolle": {"type": "string", "enum": ["gegenstand", "beispiel"]},
                },
                "required": ["beschreibung", "art", "lesbar", "rolle"],
            },
        }
    },
    "required": ["diagramme"],
}

CLASSIFY_PROMPT = """Folie {slide} aus der Vorlesung "{lecture}", Titel: "{title}".
Text der Folie (kann unvollständig sein):
---
{text}
---
Welche Diagramme sind auf der Folie abgebildet? Tabellen, Fotos, Logos und reine
Aufzählungen sind keine Diagramme. Nenne jedes Diagramm einzeln, bei keinem eine leere Liste.
Pro Diagramm:
- beschreibung: ein kurzer Satz, was es zeigt.
- art: klasse (Klassen-, Objekt-, Domänenmodell-Diagramm), sequenz, aktivitaet,
  zustand oder andere.
- lesbar: true, wenn die Beschriftungen in dieser Folienansicht sicher lesbar sind,
  false bei winzigen Miniaturen.
- rolle: "gegenstand", wenn die Folie dieses Diagramm erklärt oder bespricht und es im
  Mittelpunkt steht. "beispiel", wenn es nur Illustration ist, z. B. auf Übersichts-,
  Ausblick- oder "Verwendung von ..."-Folien oder wenn mehrere verschiedene Diagramme
  nur als Beispiele nebeneinander stehen."""

CLASSIFY_VERSION = hashlib.sha1(
    (CLASSIFY_PROMPT + json.dumps(CLASSIFY_SCHEMA, sort_keys=True)).encode("utf-8")
).hexdigest()[:8]


def is_subject(d: dict) -> bool:
    """Nur lesbare Diagramme, die Gegenstand der Folie sind, werden vollständig beschrieben."""
    return d["rolle"] == "gegenstand" and d["lesbar"]


def diagram_plan(slide: dict) -> tuple[list[str], list[str]]:
    """(Arten, die vollständig beschrieben werden, Beispielbilder als Kurztexte)"""
    override = slide.get("diagrams")  # manuelle Korrektur hat Vorrang
    if override is not None:
        arts = [a for a in override if a in DIAGRAM_RULES]
        return arts, ([] if arts else ["alle Diagramme dieser Folie (falls es welche gibt)"])
    classes = slide.get("diagram_classes") or []
    arts = list(dict.fromkeys(d["art"] for d in classes if is_subject(d)))
    examples = [d["beschreibung"] for d in classes if not is_subject(d)]
    return arts, examples


def diagram_info(slide: dict) -> str:
    arts, examples = diagram_plan(slide)
    parts = []
    if arts:
        parts.append("Diagramme, die Gegenstand dieser Folie sind, beschreibst du "
                     "vollständig nach diesen Regeln:\n"
                     + "\n".join(DIAGRAM_RULES[a] for a in arts))
    if examples:
        parts.append("Folgende Diagramme sind nur Beispielbilder und nicht Gegenstand der "
                     "Folie: " + "; ".join(examples) + ".\n" + EXAMPLE_RULE)
    return "\n".join(parts)


def plan_label(slide: dict) -> str:
    arts, examples = diagram_plan(slide)
    parts = []
    if arts:
        parts.append("voll: " + ", ".join(arts))
    if examples:
        parts.append(f"{len(examples)}x Beispiel")
    return "; ".join(parts) or "keine Diagramme"


# ---------------------------------------------------------------------------
# Kontext der Vorgängerfolie
# ---------------------------------------------------------------------------

# Vorgängerfolie mit demselben Stoff (gleicher Titel oder fast gleicher Text):
# volle Beschreibung, damit Animationsschritte einheitlich beschrieben werden.
CONTEXT_SAME = """
Die vorherige Folie zeigt sehr wahrscheinlich denselben Stoff (gleicher Titel oder
fast gleicher Text), z. B. dasselbe Diagramm in einem anderen Animationsschritt.
Ihre Beschreibung:
---
{prev_description}
---
Verwende für gleiche Elemente dieselben Namen und Elementarten, prüfe sie aber am Bild
und korrigiere Fehler. Beschreibe unter INHALT vor allem, was auf dieser Folie neu
oder anders ist (neue Hinweistexte, andere Token-Positionen, neue Elemente).
Unter ABBILDUNGEN beschreibst du das Diagramm trotzdem vollständig, damit die
Beschreibung auch für sich allein verständlich ist.
"""


# Jede andere Vorgängerfolie: nur ihr Thema, damit Bezüge verständlich sind,
# ohne dass Inhalte der vorherigen Folie in diese Beschreibung rutschen.
CONTEXT_OTHER = """
Worum es auf der vorherigen Folie ging (nur als Hintergrund, falls diese Folie
sich darauf bezieht): {prev_topic}
Beschreibe trotzdem ausschließlich, was auf DIESER Folie steht oder zu sehen ist.
Übernimm keine Inhalte von der vorherigen Folie.
"""

SIMILARITY_THRESHOLD = 0.6  # ab hier gilt der Folientext als "fast gleich"

# Zeilen, die auf fast jeder Folie einer Vorlesung stehen (Fußzeile, Kursname, Datum).
# Sie werden vor dem Vergleich entfernt, sonst wirken kurze Folien fälschlich ähnlich.
BOILERPLATE: set[str] = set()


def norm_line(line: str) -> str:
    return " ".join(re.sub(r"\d+", "#", line).split())  # Foliennummern egal


def find_boilerplate(slides: list[dict]) -> set[str]:
    counts: dict[str, int] = {}
    for s in slides:
        for line in {norm_line(l) for l in s["text"].splitlines()} - {""}:
            counts[line] = counts.get(line, 0) + 1
    if len(slides) < 4:
        return set()
    return {line for line, n in counts.items() if n >= 0.5 * len(slides)}


def content_text(text: str) -> str:
    lines = (norm_line(l) for l in text.splitlines())
    return " ".join(l for l in lines if l and l not in BOILERPLATE)


def text_similarity(a: str, b: str) -> float:
    a, b = content_text(a), content_text(b)
    if len(a) < 30 or len(b) < 30:
        return 0.0  # zu wenig Text für einen sinnvollen Vergleich
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def same_material(slide: dict, prev: dict) -> bool:
    same_title = bool(slide["title"]) and slide["title"] == prev["title"]
    return same_title or text_similarity(slide["text"], prev["text"]) >= SIMILARITY_THRESHOLD


def topic_of(description: str) -> str:
    m = re.search(r"THEMA:\s*(.+)", description)
    return (m.group(1) if m else description[:300]).strip()


def build_context(slide: dict, prev: dict | None) -> str:
    """Kontext der Vorgängerfolie: voll bei gleichem Stoff, sonst nur ihr Thema."""
    if not prev or not prev.get("description"):
        return ""
    if same_material(slide, prev):
        return CONTEXT_SAME.format(prev_description=prev["description"])
    return CONTEXT_OTHER.format(prev_topic=topic_of(prev["description"]))


# ---------------------------------------------------------------------------
# Prompt-Version und "muss beschrieben werden?"
# ---------------------------------------------------------------------------

def prompt_version(slide: dict) -> str:
    """Fingerabdruck von Kernprompt plus den Diagramm-Regeln, die diese Folie benutzt."""
    arts, examples = diagram_plan(slide)
    key = (PROMPT + CONTEXT_SAME + CONTEXT_OTHER
           + "".join(DIAGRAM_RULES[a] for a in arts)
           + (EXAMPLE_RULE if examples else ""))
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]


def classification_stale(slide: dict) -> bool:
    """Klassifikation fehlt oder stammt von einem älteren Klassifikations-Prompt."""
    return slide.get("diagrams") is None and slide.get("classify_version") != CLASSIFY_VERSION


def needs_description(slide: dict, redo: bool) -> bool:
    return (redo
            or not slide.get("description")
            or slide.get("description_prompt") != prompt_version(slide)
            or slide.get("description_hint", "") != slide.get("hint", "")
            or classification_stale(slide))


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------

def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def resolve_image(slide: dict, json_dir: Path) -> Path:
    """Sucht das Bild zuerst neben der slides.json (so legt render_slides.py es ab).

    Damit ist egal, aus welchem Ordner du die Skripte startest und ob der
    Ausgabeordner inzwischen verschoben wurde.
    """
    candidates = [
        json_dir / f"slide_{slide['slide']:03d}.png",
        json_dir / Path(slide["image"].replace("\\", "/")).name,
        Path(slide["image"]),
    ]
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError(f"Bild nicht gefunden, gesucht in {json_dir}")


def ollama_chat(args, payload: dict) -> str:
    headers = {"Authorization": f"Bearer {args.api_key}"} if args.api_key else {}
    r = requests.post(f"{args.host.rstrip('/')}/api/chat", json=payload,
                      headers=headers, timeout=args.timeout)
    if r.status_code in (401, 403):
        raise SystemExit("Zugriff verweigert: API-Key fehlt oder ist ungültig "
                         "(OPENWEBUI_API_KEY bzw. --api-key prüfen).")
    if r.status_code != 200:
        raise RuntimeError(f"Ollama antwortet {r.status_code}: {r.text[:300]}")
    content = r.json()["message"]["content"].strip()
    if not content:
        raise RuntimeError("Leere Antwort (Thinking evtl. zu lang? Versuch --no-think)")
    return content


def classify(args, slide: dict, image: Path) -> list[dict]:
    prompt = CLASSIFY_PROMPT.format(
        lecture=slide["lecture"],
        slide=slide["slide"],
        title=slide["title"] or "unbekannt",
        text=slide["text"] or "(kein Text extrahierbar)",
    )
    payload = {
        "model": args.classify_model or args.model,
        "messages": [{"role": "user", "content": prompt, "images": [encode_image(image)]}],
        "stream": False,
        "think": False,  # für die Klassifikation nicht nötig
        "format": CLASSIFY_SCHEMA,
        "options": {"temperature": 0},
        "keep_alive": "30m",
    }
    return json.loads(ollama_chat(args, payload))["diagramme"]


def ensure_classification(args, slide: dict, prev: dict | None, image: Path) -> None:
    """Klassifiziert die Diagramme der Folie, falls nötig, und speichert das Ergebnis im Dict."""
    if slide.get("diagrams") is not None:
        return  # manueller Override, keine Klassifikation nötig
    if slide.get("classify_version") == CLASSIFY_VERSION and "diagram_classes" in slide:
        return
    if (prev and "diagram_classes" in prev
            and prev.get("classify_version") == CLASSIFY_VERSION
            and same_material(slide, prev)):
        slide["diagram_classes"] = prev["diagram_classes"]  # Animationsschritt: erben
    else:
        slide["diagram_classes"] = classify(args, slide, image)
    slide["classify_version"] = CLASSIFY_VERSION


def describe(args, slide: dict, prev: dict | None, image: Path) -> str:
    prompt = PROMPT.format(
        lecture=slide["lecture"],
        slide=slide["slide"],
        prev_title=(prev or {}).get("title") or "keine",
        context=build_context(slide, prev),
        hint=("Hinweis des Autors zu dieser Folie: " + slide["hint"]) if slide.get("hint") else "",
        diagram_info=diagram_info(slide),
        text=slide["text"] or "(kein Text extrahierbar)",
    )
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt, "images": [encode_image(image)]}],
        "stream": False,
        "think": args.think,
        "options": {"temperature": 0.2},
        "keep_alive": "30m",
    }
    return ollama_chat(args, payload)


# ---------------------------------------------------------------------------
# Dateien und Hauptprogramm
# ---------------------------------------------------------------------------

def natural_key(path: Path) -> list:
    """Sortiert "Kapitel 2" vor "Kapitel 10"."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.parent.name)]


def find_slide_files(root: Path) -> list[Path]:
    """Akzeptiert den ganzen Ausgabeordner oder einen einzelnen Vorlesungsordner."""
    if (root / "slides.json").is_file():
        return [root / "slides.json"]
    return sorted(root.glob("*/slides.json"), key=natural_key)


def parse_slides(spec: str) -> set[int]:
    """'5,12-14' -> {5, 12, 13, 14}"""
    result = set()
    for part in filter(None, (p.strip() for p in spec.split(","))):
        a, _, b = part.partition("-")
        result.update(range(int(a), int(b or a) + 1))
    return result


def save_atomic(path: Path, data: list) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)  # nie eine halb geschriebene slides.json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="Ausgabeordner von render_slides.py")
    ap.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", ""),
                    help="Name wie in der Modellliste (oder OLLAMA_MODEL in .env)")
    ap.add_argument("--classify-model", default=os.environ.get("OLLAMA_CLASSIFY_MODEL", ""),
                    help="Optional: kleineres Modell für die Diagramm-Klassifikation "
                         "(sonst --model)")
    ap.add_argument("--host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
                    help="Ollama direkt, oder Open WebUI mit /ollama am Ende, "
                         "z. B. http://localhost:3000/ollama")
    ap.add_argument("--api-key", default=os.environ.get("OPENWEBUI_API_KEY", ""),
                    help="API-Key von Open WebUI (besser OPENWEBUI_API_KEY in .env, "
                         "dann steht er nicht in der Shell-History)")
    ap.add_argument("--no-think", dest="think", action="store_false",
                    help="Thinking aus: schneller, etwas weniger gründlich")
    ap.add_argument("--limit", type=int, default=0, help="Nur N Folien (zum Testen)")
    ap.add_argument("--slides", default="",
                    help="Nur diese Foliennummern, z. B. 5,12-14 (am besten mit einem "
                         "einzelnen Vorlesungsordner)")
    ap.add_argument("--redo", action="store_true",
                    help="Auch Folien mit aktuellem Prompt neu beschreiben")
    ap.add_argument("--timeout", type=int, default=900, help="Sekunden pro Folie")
    args = ap.parse_args()
    wanted = parse_slides(args.slides)
    if not args.model:
        sys.exit("Kein Modell angegeben: --model setzen oder OLLAMA_MODEL in die .env schreiben.")

    json_files = find_slide_files(args.root)
    if not json_files:
        sys.exit(f"Keine slides.json in {args.root} oder seinen Unterordnern gefunden. "
                 "Gib den Ausgabeordner von render_slides.py an.")
    print(f"{len(json_files)} Vorlesung(en): " + ", ".join(f.parent.name for f in json_files))

    todo = sum(
        1 for f in json_files for s in json.loads(f.read_text(encoding="utf-8"))
        if needs_description(s, args.redo) and (not wanted or s["slide"] in wanted)
    )
    open_total = todo
    if todo == 0:
        print("Alle ausgewählten Folien sind aktuell beschrieben, nichts zu tun. "
              "(Mit --redo trotzdem neu beschreiben.)")
        return
    if args.limit:
        todo = min(todo, args.limit)
    print(f"{open_total} Folien ohne aktuelle Beschreibung, "
          f"{'davon jetzt ' + str(todo) if todo < open_total else 'alle werden jetzt'} beschrieben "
          f"(Thinking {'an' if args.think else 'aus'}, "
          f"Klassifikation mit {args.classify_model or args.model})")
    print("Hinweis: Die erste Folie dauert länger, weil das Modell erst geladen wird.\n")

    done, errors, total_time = 0, 0, 0.0
    for jf in json_files:
        slides = json.loads(jf.read_text(encoding="utf-8"))
        BOILERPLATE.clear()
        BOILERPLATE.update(find_boilerplate(slides))
        for idx, slide in enumerate(slides):
            if args.limit and done >= args.limit:
                break
            if wanted and slide["slide"] not in wanted:
                continue
            if not needs_description(slide, args.redo):
                continue
            prev = slides[idx - 1] if idx > 0 else None
            label = f"{slide['lecture']} Folie {slide['slide']}"
            print(f"[{done + 1}/{todo}] {label} ... ", end="", flush=True)
            t0 = time.time()
            try:
                image = resolve_image(slide, jf.parent)
                ensure_classification(args, slide, prev, image)
                desc = describe(args, slide, prev, image)
            except KeyboardInterrupt:
                print("\nAbgebrochen. Fortschritt ist gespeichert.")
                return
            except Exception as e:  # einzelne Fehler sollen den Lauf nicht stoppen
                errors += 1
                print(f"FEHLER: {e}")
                continue
            secs = time.time() - t0
            slide["description"] = desc
            slide["description_model"] = args.model
            slide["description_prompt"] = prompt_version(slide)
            slide["description_hint"] = slide.get("hint", "")
            save_atomic(jf, slides)
            done += 1
            total_time += secs
            eta = (todo - done) * total_time / done / 60
            print(f"{secs:.0f}s [{plan_label(slide)}]"
                  + (f", noch ca. {eta:.0f} min" if done < todo else ""))

    print(f"Fertig: {done} beschrieben, {errors} Fehler."
          + (" Nochmal starten, um die fehlgeschlagenen nachzuholen." if errors else ""))


if __name__ == "__main__":
    main()
