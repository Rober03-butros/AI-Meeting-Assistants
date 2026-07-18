from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_verified_user
from app.schemas.audio import AudioResponse

from app.models.user import User
from app.services.audio_services import get_audio_by_id, upload_audio


router = APIRouter(
    prefix="/audio",
    tags=["Audio"],
)


@router.post("/upload",response_model=AudioResponse,)
def upload_audio_file(file: UploadFile = File(...),db: Session = Depends(get_db),current_user: User = Depends(get_verified_user)):

    return upload_audio(
        db=db,
        file=file,
    )


@router.get("/{audio_id}",response_model=AudioResponse)
def get_audio(audio_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_verified_user)):
    return get_audio_by_id(
        db=db,
        audio_id=audio_id,
    )