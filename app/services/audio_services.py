from pathlib import Path
import shutil
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.audio import Audio



UPLOAD_DIR = Path("uploads/audio")


def save_audio_file(file: UploadFile) -> str:

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    
    extension = Path(file.filename).suffix

    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)


def create_audio(db: Session,path: str) -> Audio:

    audio = Audio(path=path)

    db.add(audio)
    db.commit()
    db.refresh(audio)

    return audio


def upload_audio(db: Session, file: UploadFile) -> Audio:

    path = save_audio_file(file)

    audio = create_audio(db,path)

    return audio


def get_audio_by_id(db: Session,audio_id: int) -> Audio:

    audio = (
        db.query(Audio)
        .filter(Audio.id == audio_id)
        .first()
    )

    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio not found",
        )

    return audio