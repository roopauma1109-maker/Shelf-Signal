import json
import re
from pathlib import Path

INPUT_FILE = Path("data/processed/documents.jsonl")
OUTPUT_FILE = Path("data/processed/chunks.jsonl")

CHUNK_SIZE = 250
CHUNK_OVERLAP = 40


def split_sentences(text: str) -> list[str]:
    """Split paragraph into sentence-like units."""
    sentences = re.split(
        r'(?<=[.!?])\s+(?=[A-Z0-9“"(\[])',
        text.strip()
    )

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def get_text_units(text: str) -> list[str]:
    """Split text into paragraphs, then sentences."""
    paragraphs = re.split(r"\n\s*\n+", text.strip())

    units = []

    for paragraph in paragraphs:
        paragraph = re.sub(r"\s+", " ", paragraph).strip()

        if not paragraph:
            continue

        units.extend(split_sentences(paragraph))

    return units


def split_into_chunks(text: str) -> list[str]:
    units = get_text_units(text)

    if not units:
        return []

    chunks = []
    current_units = []
    current_words = 0

    for unit in units:
        unit_word_count = len(unit.split())

        # Handle an exceptionally long sentence.
        if unit_word_count > CHUNK_SIZE:
            if current_units:
                chunks.append(" ".join(current_units))
                current_units = []
                current_words = 0

            words = unit.split()

            start = 0
            while start < len(words):
                end = min(start + CHUNK_SIZE, len(words))
                chunks.append(" ".join(words[start:end]))

                if end == len(words):
                    break

                start = end - CHUNK_OVERLAP

            continue

        if current_words + unit_word_count > CHUNK_SIZE:
            chunks.append(" ".join(current_units))

            # Retain recent sentences for context overlap.
            overlap_units = []
            overlap_words = 0

            for previous_unit in reversed(current_units):
                count = len(previous_unit.split())

                if overlap_words + count > CHUNK_OVERLAP:
                    break

                overlap_units.insert(0, previous_unit)
                overlap_words += count

            current_units = overlap_units
            current_words = overlap_words

        current_units.append(unit)
        current_words += unit_word_count

    if current_units:
        chunks.append(" ".join(current_units))

    return chunks


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total_chunks = 0

    with (
        INPUT_FILE.open("r", encoding="utf-8") as source,
        OUTPUT_FILE.open("w", encoding="utf-8") as output,
    ):
        for line in source:
            if not line.strip():
                continue

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