from datetime import datetime

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str



class SourceResponse(BaseModel):
    start: float
    end: float


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]


class ChatMessageResponse(BaseModel):
    id: int
    question: str
    answer: str | None
    sources: list[SourceResponse]
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageResponse]

