from PyPDF2 import PdfReader

reader = PdfReader("long_sample_with_comments.pdf")

annotations = []
for page_idx, page in enumerate(reader.pages):
    annots = page.get("/Annots") or []
    for a in annots:
        obj = a.get_object()
        if obj.get("/Subtype") == "/Text":
            annotations.append({
                "page": page_idx + 1,
                "comment": obj.get("/Contents"),
                "rect": obj.get("/Rect")
            })

            