"""
Rendert alle Seiten von Vorlesungs-PDFs als PNG und extrahiert den Text.

Installation:  pip install pymupdf
Aufruf:        python render_slides.py folien/ ausgabe/

Ergebnis pro PDF:
    ausgabe/<pdf-name>/slide_001.png, slide_002.png, ...
    ausgabe/<pdf-name>/slides.json   (Text, Titel und Metadaten pro Folie)

Erneutes Ausführen ist ungefährlich:
- Das Feld "hint" (Hinweis des Autors für die Beschreibung) bleibt erhalten.
  Es wird nach Foliennummer übernommen. Wenn sich im PDF Folien verschieben,
  die Hints prüfen.
- Vorhandene Beschreibungen (description, description_model, description_prompt,
  description_hint) bleiben nur erhalten, wenn der extrahierte Folientext
  unverändert ist. Sonst wird die Folie beim nächsten Lauf von
  describe_slides.py neu beschrieben.
"""

import json
import os
import sys
from pathlib import Path

import pymupdf  # PyMuPDF

DPI = 150  # guter Kompromiss: scharf genug für Formeln, nicht zu viele Bild-Tokens

# Felder, die describe_slides.py schreibt und die hier nicht verloren gehen sollen
DESCRIPTION_KEYS = ("description", "description_model", "description_prompt", "description_hint",
                    "diagram_classes", "classify_version")


def guess_title(page: pymupdf.Page) -> str:
    """Nimmt den Text mit der größten Schrift in der oberen Seitenhälfte als Titel."""
    best_size, best_text = 0.0, ""
    half = page.rect.height / 2
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            if line["bbox"][1] > half:
                continue
            text = " ".join(s["text"] for s in line["spans"]).strip()
            size = max((s["size"] for s in line["spans"]), default=0)
            if text and size > best_size:
                best_size, best_text = size, text
    return best_text


def load_previous(json_path: Path) -> dict[int, dict]:
    """Liest eine vorhandene slides.json, damit Hints und Beschreibungen erhalten bleiben."""
    if not json_path.is_file():
        return {}
    try:
        return {s["slide"]: s for s in json.loads(json_path.read_text(encoding="utf-8"))}
    except (json.JSONDecodeError, KeyError, TypeError):
        print(f"Warnung: {json_path} nicht lesbar, Hints und Beschreibungen können "
              "nicht übernommen werden.")
        return {}


def save_atomic(path: Path, data: list) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)  # nie eine halb geschriebene slides.json


def process_pdf(pdf_path: Path, out_root: Path) -> None:
    out_dir = out_root / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "slides.json"
    old = load_previous(json_path)
    slides = []
    kept_desc, kept_hints = 0, 0

    # loops over pdf pages
    with pymupdf.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            # render the image
            image_path = out_dir / f"slide_{i:03d}.png"
            page.get_pixmap(dpi=DPI).save(image_path)
            # extract the text
            text = page.get_text("text", sort=True).strip()  # sort=True: Lesereihenfolge

            entry = {
                "lecture": pdf_path.stem,
                "slide": i,
                "title": guess_title(page),
                "text": text,
                "image": str(image_path),
                "has_text": bool(text),
                "hint": "",  # optional: Hinweis des Autors für die Beschreibung
            }

            prev = old.get(i, {})
            # Hint immer übernehmen (er ist Handarbeit)
            entry["hint"] = prev.get("hint", "")
            if entry["hint"]:
                kept_hints += 1
            # Manueller Override der Diagrammarten ebenfalls immer übernehmen
            if "diagrams" in prev:
                entry["diagrams"] = prev["diagrams"]
            # Beschreibung nur übernehmen, wenn die Folie unverändert ist
            if prev.get("text") == text:
                had = False
                for key in DESCRIPTION_KEYS:
                    if key in prev:
                        entry[key] = prev[key]
                        had = had or key == "description"
                kept_desc += had

            slides.append(entry)

    save_atomic(json_path, slides)
    no_text = sum(not s["has_text"] for s in slides)
    print(f"{pdf_path.name}: {len(slides)} Folien"
          + (f", davon {no_text} ohne Text (gescannt/nur Bild)" if no_text else "")
          + (f", {kept_desc} Beschreibungen übernommen" if kept_desc else "")
          + (f", {kept_hints} Hints übernommen" if kept_hints else ""))


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Aufruf: python render_slides.py <pdf-ordner> <ausgabe-ordner>")
    pdf_dir, out_root = Path(sys.argv[1]), Path(sys.argv[2])
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"Keine PDFs in {pdf_dir} gefunden.")
    for pdf in pdfs:
        process_pdf(pdf, out_root)


if __name__ == "__main__":
    main()
