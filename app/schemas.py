from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Question about FMCG company reports",
    )
    company: str | None = Field(
        default=None,
        description="Optional company filter",
    )


class Citation(BaseModel):
    company: str
    report: str
    page: int
    similarity_score: float


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]