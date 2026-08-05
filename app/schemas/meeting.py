from datetime import datetime
from pydantic import BaseModel


class MeetingCreate(BaseModel):
    title: str


class MeetingResponse(BaseModel):
    id: int
    title : str
    created_at: datetime

    class Config:
        from_attributes = True

class Meeting_transcript_Response(BaseModel):
    id: int
    title : str
    created_at: datetime
    transcript: str


    class Config:
        from_attributes = True

class Meetings_Response(BaseModel):
    id: int
    title : str
    created_at: datetime

    class Config:
        from_attributes = True