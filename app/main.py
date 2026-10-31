
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.schemas import ChatRequest, ChatResponse, Citation
from app.search import search

app = FastAPI(
    title="ShelfSignal API",
    description="Low-bandwidth FMCG annual report research assistant",
    version="1.0.0",
)

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    return {
        "status": "ok",
        "app": "ShelfSignal",
        "environment": settings.environment,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        results = search(
            question=request.question,
            top_k=5,
            company=request.company,
        )

        if not results:
            return ChatResponse(
                answer="No relevant information was found in the reports.",
                citations=[],
            )

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

        # Temporary retrieval-only response.
        # LLM generation will be added in the next step.
        answer = (
            "Relevant information was retrieved from the annual reports. "
            "LLM-based answer generation will be added next."
        )

        return ChatResponse(
            answer=answer,
            citations=citations,
        )

    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error
