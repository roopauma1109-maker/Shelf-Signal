
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = Path("data/processed")
INDEX_FILE = DATA_DIR / "faiss.index"
METADATA_FILE = DATA_DIR / "chunks_metadata.jsonl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_metadata() -> list[dict]:
    with METADATA_FILE.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def search(
    question: str,
    top_k: int = 5,
) -> list[dict]:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        raise FileNotFoundError(
            "Index or metadata not found. Run embeddings first."
        )

    index = faiss.read_index(str(INDEX_FILE))
    metadata = load_metadata()

    if index.ntotal != len(metadata):
        raise ValueError(
            "FAISS index and metadata record counts do not match."
        )

    model = SentenceTransformer(MODEL_NAME)
    question_vector = model.encode(
        [question],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    scores, indices = index.search(
        question_vector.astype("float32"),
        min(top_k, index.ntotal),
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        result = metadata[int(idx)].copy()
        result["similarity_score"] = float(score)
        results.append(result)

    return results


if __name__ == "__main__":
    question = input("Enter your question: ")
    results = search(question)

    for number, result in enumerate(results, start=1):
        print(f"\n--- Result {number} ---")
        print("Company:", result["company"])
        print("Report:", result["source_file"])
        print("Page:", result["page_number"])
        print("Similarity:", round(result["similarity_score"], 4))
        print("Text:", result["text"][:500])
