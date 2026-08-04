from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str



class SourceResponse(BaseModel):
    start: float
    end: float



class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]

