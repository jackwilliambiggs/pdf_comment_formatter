from PyPDF2 import PdfReader
import pdfplumber
import re
from pprint import pprint

PDF_PATH = "long_sample_with_comments.pdf"

# ============================================================
# Coordinate helpers
# ============================================================

def pypdf_rect_to_pdfplumber(rect, page_height):
    """
    Convert PyPDF2 annotation rect (bottom-left origin)
    to pdfplumber coordinates (top-left origin).

    rect: [x0, y0, x1, y1] (PyPDF2 FloatObjects)
    """
    x0, y0, x1, y1 = map(float, rect)

    return {
        "x0": x0,
        "x1": x1,
        "top": page_height - y1,
        "bottom": page_height - y0,
    }


def rects_intersect(a, b):
    """
    Intersection between:
      a: dict {x0, x1, top, bottom}
      b: tuple (x0, top, x1, bottom)
    """
    return not (
        a["x1"] < b[0] or
        a["x0"] > b[2] or
        a["bottom"] < b[1] or
        a["top"] > b[3]
    )


# ============================================================
# Extract annotations (comments)
# ============================================================

def extract_annotations(pdf_path):
    reader = PdfReader(pdf_path)
    annotations = []

    for page_idx, page in enumerate(reader.pages):
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if obj.get("/Subtype") == "/Text":
                annotations.append({
                    "page": page_idx + 1,
                    "comment": str(obj.get("/Contents")),
                    "rect": obj.get("/Rect")
                })

    return annotations


# ============================================================
# Extract sentences with layout data
# ============================================================

def extract_sentences_with_positions(pdf_path):
    """
    Returns:
    {
        page_number: [
            { "text": sentence, "rect": (x0, top, x1, bottom) }
        ]
    }
    """
    sentence_map = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(use_text_flow=True)
            words.sort(key=lambda w: (w["top"], w["x0"]))

            lines = []
            current = []
            last_top = None

            for w in words:
                if last_top is None or abs(w["top"] - last_top) < 3:
                    current.append(w)
                else:
                    lines.append(current)
                    current = [w]
                last_top = w["top"]

            if current:
                lines.append(current)

            sentences = []

            for line in lines:
                text = " ".join(w["text"] for w in line)
                rect = (
                    min(w["x0"] for w in line),
                    min(w["top"] for w in line),
                    max(w["x1"] for w in line),
                    max(w["bottom"] for w in line),
                )

                for s in re.split(r"(?<=[.!?])\s+", text):
                    if s.strip():
                        sentences.append({
                            "text": s.strip(),
                            "rect": rect
                        })

            sentence_map[page_num] = sentences

    return sentence_map


# ============================================================
# Map annotations → sentences
# ============================================================

def map_comments_to_sentences(pdf_path, annotations, sentence_map):
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for ann in annotations:
            page_idx = ann["page"] - 1
            page = pdf.pages[page_idx]

            ann_rect = pypdf_rect_to_pdfplumber(
                ann["rect"],
                page.height
            )

            matched_sentence = None

            for sentence in sentence_map.get(ann["page"], []):
                if rects_intersect(ann_rect, sentence["rect"]):
                    matched_sentence = sentence["text"]
                    break

            results.append({
                "page": ann["page"],
                "comment": ann["comment"],
                "sentence": matched_sentence
            })

    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("\n🔍 Extracting annotations...")
    annotations = extract_annotations(PDF_PATH)

    print("\n📄 Extracting sentences...")
    sentence_map = extract_sentences_with_positions(PDF_PATH)

    print("\n🧠 Mapping comments to sentences...")
    results = map_comments_to_sentences(
        PDF_PATH,
        annotations,
        sentence_map
    )

    print("\n✅ FINAL OUTPUT:\n")
    pprint(results)
