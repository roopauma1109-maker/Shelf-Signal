
import json
from pathlib import Path

import pymupdf

DATA_DIR = Path("data/sample")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "documents.jsonl"


def extract_pdf(pdf_path: Path) -> list[dict]:
    documents = []

    with pymupdf.open(pdf_path) as pdf:
        company = pdf_path.parent.name
        report_year = "2025-26"

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()

            if not text:
                continue

            documents.append(
                {
                    "company": company,
                    "report_year": report_year,
                    "page_number": page_number,
                    "source_file": pdf_path.name,
                    "text": text,
                }
            )

    return documents


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(DATA_DIR.rglob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {DATA_DIR}")
        return

    total_pages = 0
    total_documents = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for pdf_path in pdf_files:
            try:
                documents = extract_pdf(pdf_path)

                for document in documents:
                    output.write(
                        json.dumps(document, ensure_ascii=False) + "\n"
                    )

                total_documents += len(documents)

                with pymupdf.open(pdf_path) as pdf:
                    total_pages += len(pdf)

                print(
                    f"{pdf_path.parent.name}: "
                    f"{len(documents)} pages extracted"
                )

            except Exception as error:
                print(f"ERROR processing {pdf_path}: {error}")

    print(f"\nTotal PDF pages: {total_pages}")
    print(f"Pages with extracted text: {total_documents}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
