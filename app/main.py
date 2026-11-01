
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.llm import generate_answer
from app.schemas import ChatRequest, ChatResponse, Citation
from app.search import search

app = FastAPI(
    title="ShelfSignal API",
    description="FMCG Annual Report Research Assistant",
    version="1.0.0",
)

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    # Step 1: Retrieve relevant report chunks
    try:
        results = search(
            question=request.question,
            top_k=5,
            company=request.company,
        )
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    if not results:
        return ChatResponse(
            answer="No relevant information was found in the reports.",
            citations=[],
        )

    # Step 2: Generate an answer using Gemini
    try:
        answer = generate_answer(
            question=request.question,
            retrieved_chunks=results,
        )
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini answer generation failed: {error}",
        ) from error

    # Step 3: Prepare source citations
    citations = [
        Citation(
            company=result["company"],
            report=result["source_file"],
            page=result["page_number"],
            similarity_score=round(
                result["similarity_score"], 4
            ),
        )
        for result in results
    ]

    return ChatResponse(
        answer=answer,
        citations=citations,
    )
