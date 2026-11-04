import json
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.config import Settings, get_settings
from app.llm import generate_answer, stream_answer
from app.schemas import ChatRequest, ChatResponse, Citation
from app.search import search
from app.usage import get_usage_summary

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


@app.get("/usage")
def usage() -> dict:
    return get_usage_summary()


def get_citations(results: list[dict]) -> list[Citation]:
    return [
        Citation(
            company=result["company"],
            report=result["source_file"],
            page=result["page_number"],
            similarity_score=round(result["similarity_score"], 4),
        )
        for result in results
    ]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

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

    return ChatResponse(
        answer=answer,
        citations=get_citations(results),
    )


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

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

    citations = get_citations(results)

    def generate_events():
        try:
            for text in stream_answer(
                question=request.question,
                retrieved_chunks=results,
            ):
                event_data = json.dumps({"text": text})
                yield f"event: token\ndata: {event_data}\n\n"

            citation_data = json.dumps([citation.model_dump() for citation in citations])

            yield f"event: citations\ndata: {citation_data}\n\n"
            yield "event: done\ndata: {}\n\n"

        except Exception as error:
            error_data = json.dumps({"message": str(error)})
            yield f"event: error\ndata: {error_data}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
