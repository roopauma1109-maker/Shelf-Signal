
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INPUT_FILE = Path("data/processed/chunks.jsonl")
OUTPUT_DIR = Path("data/processed")
INDEX_FILE = OUTPUT_DIR / "faiss.index"
METADATA_FILE = OUTPUT_DIR / "chunks_metadata.jsonl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Chunks file not found: {INPUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chunks = []
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            if record.get("text", "").strip():
                chunks.append(record)

    if not chunks:
        raise ValueError("No non-empty chunks found.")

    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    texts = [record["text"] for record in chunks]

    print(f"Creating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_FILE))

    with METADATA_FILE.open("w", encoding="utf-8") as file:
        for record in chunks:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Embeddings created: {embeddings.shape}")
    print(f"FAISS index saved: {INDEX_FILE}")
    print(f"Metadata saved: {METADATA_FILE}")


if __name__ == "__main__":
    main()
