
from pathlib import Path

import fitz


def extract_pdf_text(pdf_path):
    pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text
                })

    return pages


if __name__ == "__main__":
    pdf_path = Path("data/sample/HUL/HUL-2025-26.pdf")

    if not pdf_path.exists():
        print("PDF not found:", pdf_path)
    else:
        pages = extract_pdf_text(pdf_path)

        print("PDF:", pdf_path.name)
        print("Pages with text:", len(pages))

        for page in pages[:2]:
            print(f"\nPage {page['page']}:")
            print(page["text"][:500])
