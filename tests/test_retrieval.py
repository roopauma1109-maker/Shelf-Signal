import json

import faiss
import numpy as np
import pytest

import app.search as search_module


class FakeEmbeddingModel:
    """Return a predictable embedding for CI tests."""

    def encode(
        self,
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ):
        return np.array([[1.0, 0.0]], dtype="float32")


@pytest.fixture
def test_search_data(tmp_path, monkeypatch):
    records = [
        {
            "company": "Britannia",
            "page_number": 36,
            "source_file": "Britannia-2025-26-report.pdf",
            "chunk_id": "Britannia_36_5",
            "text": (
                "Rural markets are a key growth driver. "
                "Britannia focuses on Rural Preferred Dealers, "
                "small value packs, last-mile distribution, "
                "and affordable products."
            ),
        },
        {
            "company": "HUL",
            "page_number": 46,
            "source_file": "HUL-report.pdf",
            "chunk_id": "HUL_46_1",
            "text": "Urban product development and marketing strategy.",
        },
        {
            "company": "ITC",
            "page_number": 82,
            "source_file": "ITC-report.pdf",
            "chunk_id": "ITC_82_1",
            "text": "Manufacturing operations and financial performance.",
        },
    ]

    metadata_file = tmp_path / "chunks_metadata.jsonl"
    index_file = tmp_path / "faiss.index"

    with metadata_file.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    vectors = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [-1.0, 0.0],
        ],
        dtype="float32",
    )

    index = faiss.IndexFlatIP(2)
    index.add(vectors)

    faiss.write_index(index, str(index_file))

    monkeypatch.setattr(
        search_module,
        "INDEX_FILE",
        index_file,
    )
    monkeypatch.setattr(
        search_module,
        "METADATA_FILE",
        metadata_file,
    )
    monkeypatch.setattr(
        search_module,
        "get_model",
        lambda: FakeEmbeddingModel(),
    )


@pytest.mark.parametrize(
    "question",
    [
        "What are Britannia's strategies for rural market penetration?",
        "How does Britannia use affordable packs to increase rural sales?",
        "Explain Britannia's Rural Preferred Dealer strategy.",
    ],
)
def test_rural_evidence_retrieval(
    question,
    test_search_data,
):
    results = search_module.search(
        question,
        top_k=3,
        company="Britannia",
    )

    assert results

    assert results[0]["company"] == "Britannia"
    assert results[0]["page_number"] == 36

    assert "Rural Preferred Dealers" in results[0]["text"]


def test_company_filter(test_search_data):
    results = search_module.search(
        "What is the company strategy?",
        top_k=5,
        company="HUL",
    )

    assert results
    assert all(result["company"] == "HUL" for result in results)


def test_empty_question():
    with pytest.raises(ValueError, match="Question cannot be empty"):
        search_module.search("")


def test_invalid_top_k():
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        search_module.search("rural market", top_k=0)