
import json
from pathlib import Path

INPUT_FILE = Path("data/processed/documents.jsonl")
OUTPUT_FILE = Path("data/processed/chunks.jsonl")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_into_chunks(text: str) -> list[str]:
    words = text.split()
    chunks = []

    if not words:
        return chunks

    start = 0

    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    total_chunks = 0

    with (
        INPUT_FILE.open("r", encoding="utf-8") as source,
        OUTPUT_FILE.open("w", encoding="utf-8") as output,
    ):
        for line in source:
            document = json.loads(line)
            chunks = split_into_chunks(document["text"])

            for index, chunk in enumerate(chunks, start=1):
                record = {
                    "company": document["company"],
                    "report_year": document["report_year"],
                    "page_number": document["page_number"],
                    "source_file": document["source_file"],
                    "chunk_id": (
                        f'{document["company"]}_'
                        f'{document["page_number"]}_{index}'
                    ),
                    "chunk_index": index,
                    "text": chunk,
                }

                output.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )
                total_chunks += 1

    print(f"Total chunks created: {total_chunks}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
