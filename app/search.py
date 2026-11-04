
import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


DATA_DIR = Path("data/processed")
INDEX_FILE = DATA_DIR / "faiss.index"
METADATA_FILE = DATA_DIR / "chunks_metadata.jsonl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

K1 = 1.5
B = 0.75
RRF_K = 60

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "how", "what", "why", "when", "where", "who",
    "does", "do", "did", "has", "have", "had",
    "and", "or", "but", "in", "on", "at", "to",
    "of", "for", "from", "with", "by", "its",
    "their", "it", "this", "that", "across",
    "company", "companies"
}

QUERY_SYNONYMS = {
    "rural": ["village", "villages", "distribution"],
    "market": ["markets", "availability", "network"],
    "expand": ["expansion", "strengthen", "widespread"],
    "expanding": ["expansion", "strengthen", "widespread"],
    "distribution": ["network", "availability", "reach"],
    "availability": ["distribution", "widespread", "reach"],
    "village": ["villages", "rural"],
}


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load and cache the embedding model."""
    return SentenceTransformer(MODEL_NAME)


def load_metadata() -> list[dict]:
    """Load metadata records from JSONL."""
    with METADATA_FILE.open("r", encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


def tokenize(text: str) -> list[str]:
    """Normalize text into searchable lowercase tokens."""

    words = re.findall(r"[a-z0-9]+", text.lower())
    tokens = []

    for word in words:
        if word in STOPWORDS or len(word) <= 1:
            continue

        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"

        elif (
            word.endswith("s")
            and not word.endswith("ss")
            and len(word) > 4
        ):
            word = word[:-1]

        tokens.append(word)

    return tokens


def expand_query(question: str) -> list[str]:
    """Expand query with domain-specific synonyms."""

    query_tokens = tokenize(question)
    expanded_tokens = list(query_tokens)

    for token in query_tokens:
        expanded_tokens.extend(
            QUERY_SYNONYMS.get(token, [])
        )

    return list(dict.fromkeys(expanded_tokens))


def bm25_search(
    question: str,
    records: list[dict],
) -> list[tuple[int, float]]:
    """Calculate BM25 keyword relevance."""

    if not records:
        return []

    query_tokens = expand_query(question)

    if not query_tokens:
        return []

    documents = [
        tokenize(record.get("text", ""))
        for record in records
    ]

    document_lengths = [
        len(document)
        for document in documents
    ]

    average_length = (
        sum(document_lengths) / len(document_lengths)
    )

    if average_length == 0:
        return []

    document_frequency = Counter()

    for document in documents:
        document_frequency.update(set(document))

    total_documents = len(documents)
    scores = []

    for idx, document in enumerate(documents):

        term_frequency = Counter(document)
        document_length = document_lengths[idx]
        score = 0.0

        for term in query_tokens:

            frequency = term_frequency.get(term, 0)

            if frequency == 0:
                continue

            df = document_frequency.get(term, 0)

            idf = math.log(
                1 + (
                    total_documents - df + 0.5
                ) / (df + 0.5)
            )

            denominator = frequency + K1 * (
                1 - B + B * document_length / average_length
            )

            score += idf * (
                frequency * (K1 + 1) / denominator
            )

        scores.append((idx, score))

    return sorted(
        scores,
        key=lambda item: item[1],
        reverse=True,
    )


def search(
    question: str,
    top_k: int = 50,
    company: str | None = None,
) -> list[dict]:
    """Hybrid retrieval using FAISS, BM25 and RRF."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"FAISS index not found: {INDEX_FILE}"
        )

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}"
        )

    index = faiss.read_index(str(INDEX_FILE))
    metadata = load_metadata()

    if index.ntotal != len(metadata):
        raise ValueError(
            "FAISS index and metadata record counts do not match."
        )

    if index.ntotal == 0:
        return []

    # -----------------------------------------
    # 1. Company filtering
    # -----------------------------------------

    eligible_indices = [
        idx
        for idx, record in enumerate(metadata)
        if (
            not company
            or str(record.get("company", "")).casefold()
            == company.strip().casefold()
        )
    ]

    if not eligible_indices:
        return []

    eligible_set = set(eligible_indices)

    # -----------------------------------------
    # 2. Query embedding
    # -----------------------------------------

    model = get_model()

    question_vector = model.encode(
        [question.strip()],
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype("float32")

    if question_vector.shape[1] != index.d:
        raise ValueError(
            "Query and FAISS embedding dimensions do not match."
        )

    # -----------------------------------------
    # 3. Semantic search using FAISS
    # -----------------------------------------

    scores, indices = index.search(
        question_vector,
        index.ntotal,
    )

    semantic_rank = {}

    rank = 0

    for score, idx in zip(
        scores[0],
        indices[0],
        strict=True,
    ):

        idx = int(idx)

        if idx not in eligible_set:
            continue

        rank += 1

        semantic_rank[idx] = (
            rank,
            float(score),
        )

    # -----------------------------------------
    # 4. Keyword search using BM25
    # -----------------------------------------

    eligible_records = [
        metadata[idx]
        for idx in eligible_indices
    ]

    keyword_results = bm25_search(
        question,
        eligible_records,
    )

    keyword_rank = {}

    for rank, (local_idx, score) in enumerate(
        keyword_results,
        start=1,
    ):

        original_idx = eligible_indices[local_idx]

        keyword_rank[original_idx] = (
            rank,
            score,
        )

    # -----------------------------------------
    # 5. Reciprocal Rank Fusion
    # -----------------------------------------

    combined_results = []

    for idx in eligible_indices:

        semantic_info = semantic_rank.get(idx)
        keyword_info = keyword_rank.get(idx)

        semantic_score = (
            semantic_info[1]
            if semantic_info
            else 0.0
        )

        keyword_score = (
            keyword_info[1]
            if keyword_info
            else 0.0
        )

        hybrid_score = 0.0

        if semantic_info:
            hybrid_score += 1 / (
                RRF_K + semantic_info[0]
            )

        if keyword_info:
            hybrid_score += 1 / (
                RRF_K + keyword_info[0]
            )

        result = metadata[idx].copy()

        result["similarity_score"] = semantic_score
        result["keyword_score"] = keyword_score
        result["hybrid_score"] = hybrid_score

        combined_results.append(result)

    # -----------------------------------------
    # 6. Final ranking
    # -----------------------------------------

    combined_results.sort(
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )

    return combined_results[:top_k]


if __name__ == "__main__":

    question = input("Enter your question: ").strip()

    company = input(
        "Company filter "
        "(Britannia, HUL, ITC, Dabur, Marico, Nestle_India; "
        "press Enter for all): "
    ).strip() or None

    try:

        results = search(
            question=question,
            top_k=50,
            company=company,
        )

        if not results:
            print("\nNo matching results found.")

        for number, result in enumerate(
            results,
            start=1,
        ):

            print(f"\n--- Result {number} ---")
            print("Company:", result.get("company"))
            print("Page:", result.get("page_number"))
            print("Chunk ID:", result.get("chunk_id"))

            print(
                "Semantic:",
                round(result["similarity_score"], 4),
            )

            print(
                "Keyword:",
                round(result["keyword_score"], 4),
            )

            print(
                "Hybrid:",
                round(result["hybrid_score"], 6),
            )

            print(
                "Text:",
                result.get("text", "")[:350],
            )

    except (ValueError, FileNotFoundError) as error:
        print("Error:", error)
