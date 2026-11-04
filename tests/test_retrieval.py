import pytest

from app.search import search


@pytest.mark.parametrize(
    "question, expected_company, expected_page",
    [
        (
            "What are Britannia's strategies for rural market penetration?",
            "Britannia",
            36,
        ),
        (
            "How does Britannia use affordable packs to increase rural sales?",
            "Britannia",
            36,
        ),
        (
            "Explain Britannia's Rural Preferred Dealer strategy.",
            "Britannia",
            36,
        ),
    ],
)
def test_rural_evidence_retrieval(
    question,
    expected_company,
    expected_page,
):
    results = search(
        question,
        top_k=5,
        company=expected_company,
    )

    assert results, f"No results returned for: {question}"

    matching_result = any(
        result["company"] == expected_company
        and result["page_number"] == expected_page
        for result in results
    )

    assert matching_result, (
        f"Expected evidence from {expected_company}, "
        f"page {expected_page}, not found in top 5."
    )