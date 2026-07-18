from datetime import datetime

from pydantic import BaseModel


class AudioResponse(BaseModel):
    id: int
    path: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }