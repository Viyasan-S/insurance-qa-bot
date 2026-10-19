
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500,
        description="Question about the mock life insurance policy",
    )


class SourceReference(BaseModel):
    source: str
    page: int


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]
    notice: str
