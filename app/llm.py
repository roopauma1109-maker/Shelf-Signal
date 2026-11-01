
from google import genai
from google.genai import types

from app.config import get_settings


def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    if not retrieved_chunks:
        return "No relevant information was found in the reports."

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

    prompt = f"""
You are ShelfSignal, an FMCG annual report research assistant.

Answer using ONLY the provided annual report context.

Instructions:
- Do not invent facts, figures, or strategies.
- If the context does not contain the answer, say so.
- Give a clear and concise answer.
- Use simple business language.
- Mention relevant company names and page numbers.
- Focus on FMCG growth, rural distribution, pricing and market strategies.

REPORT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

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
