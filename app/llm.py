
from collections.abc import Iterator

from google import genai
from google.genai import types

from app.config import get_settings


def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Company: {chunk["company"]}
Report: {chunk["source_file"]}
Page: {chunk["page_number"]}

Content:
{chunk["text"]}
"""
        )

    context = "\n\n".join(context_parts)
    print(f"Gemini context size: {len(context)} characters")

    return f"""
You are ShelfSignal, an FMCG annual report research assistant.

Answer using ONLY the provided annual report context.

Instructions:
- Do not invent facts, figures, or strategies.
- If the context does not contain the answer, say so.
- Give a clear and concise answer.
- Use simple business language.
- Mention relevant company names and page numbers.
- Focus on FMCG growth, rural distribution, pricing and market strategies.
- Clearly distinguish missing retrieved information from information absent in the full report.

REPORT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


def create_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(
            timeout=120000,
            retry_options=types.HttpRetryOptions(
                attempts=2,
                initial_delay=1,
                max_delay=5,
                http_status_codes=[408, 429, 500, 502, 503, 504],
            ),
        ),
    )

    return client, settings


def generate_answer(
    question: str,
    retrieved_chunks: list[dict],
) -> str:
    if not retrieved_chunks:
        return "No relevant information was found in the reports."

    client, settings = create_client()
    prompt = build_prompt(question, retrieved_chunks)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=512,
                thinking_config=types.ThinkingConfig(
                    thinking_level="LOW"
                ),
            ),
        )

        answer = response.text

        if not answer:
            raise ValueError("Gemini returned an empty response.")

        return answer.strip()

    finally:
        client.close()


def stream_answer(
    question: str,
    retrieved_chunks: list[dict],
) -> Iterator[str]:
    if not retrieved_chunks:
        yield "No relevant information was found in the reports."
        return

    client, settings = create_client()
    prompt = build_prompt(question, retrieved_chunks)

    try:
        response_stream = client.models.generate_content_stream(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=512,
                thinking_config=types.ThinkingConfig(
                    thinking_level="LOW"
                ),
            ),
        )

        received_text = False

        for chunk in response_stream:
            text = chunk.text

            if text:
                received_text = True
                yield text

        if not received_text:
            raise ValueError("Gemini returned an empty streaming response.")

    finally:
        client.close()
