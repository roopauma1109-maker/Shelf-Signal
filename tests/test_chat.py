from unittest.mock import patch


def test_chat_success(client):
    mock_results = [
        {
            "company": "Britannia",
            "source_file": "Britannia-2025-26-report.pdf",
            "page_number": 36,
            "similarity_score": 0.85,
        }
    ]

    with (
        patch("app.main.search", return_value=mock_results),
        patch(
            "app.main.generate_answer",
            return_value="Britannia uses Rural Preferred Dealers and affordable packs.",
        ),
    ):
        response = client.post(
            "/chat",
            json={
                "question": "How does Britannia expand rural sales?",
                "company": "Britannia",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "Rural Preferred Dealers" in data["answer"]
    assert len(data["citations"]) == 1
    assert data["citations"][0]["company"] == "Britannia"
    assert data["citations"][0]["page"] == 36


def test_chat_no_results(client):
    with patch("app.main.search", return_value=[]):
        response = client.post(
            "/chat",
            json={
                "question": "Explain an unrelated topic."
            },
        )

    assert response.status_code == 200
    assert response.json()["citations"] == []
    assert response.json()["answer"] == (
        "No relevant information was found in the reports."
    )


def test_chat_gemini_failure(client):
    mock_results = [
        {
            "company": "Britannia",
            "source_file": "Britannia-2025-26-report.pdf",
            "page_number": 36,
            "similarity_score": 0.85,
        }
    ]

    with (
        patch("app.main.search", return_value=mock_results),
        patch(
            "app.main.generate_answer",
            side_effect=Exception("Mock Gemini failure"),
        ),
    ):
        response = client.post(
            "/chat",
            json={
                "question": "How does Britannia expand rural sales?"
            },
        )

    assert response.status_code == 502
    assert "Gemini answer generation failed" in response.json()["detail"]