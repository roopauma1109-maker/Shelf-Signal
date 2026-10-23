
from app.pdf_reader import extract_pdf_text
from pathlib import Path

pdf_path = Path("data/sample/HUL/HUL-2025-26.pdf")
pages = extract_pdf_text(pdf_path)

keywords = [
    "rural",
    "rural demand",
    "rural growth",
    "rural markets",
    "rural consumption",
    "village",
    "price reduction",
    "price cuts",
    "volume growth",
    "demand recovery"
]

for page in pages:
    text = page["text"]
    lower_text = text.lower()

    matched = [word for word in keywords if word in lower_text]

    if matched:
        print(f"\n--- PDF Page {page['page']} ---")
        print("Keywords:", ", ".join(matched))
        print(text[:1000])

