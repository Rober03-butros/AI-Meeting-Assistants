from fastapi import APIRouter, Form, HTTPException
from pathlib import Path

from fastapi import UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_verified_user
from app.models.meeting import Meeting
from app.models.meeting_user import MeetingUser
from app.models.user import User

from app.schemas.meeting import MeetingResponse
from app.services.meeting_services import create_meeting, delete_meeting, get_meeting_by_id, get_meeting_owner,get_user_meetings


router = APIRouter(
    prefix="/meetings",
    tags=["meetings"],
    dependencies=[Depends(get_verified_user)]
)


@router.post("/upload",response_model=MeetingResponse,)
def upload_meeting_audio(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):

    return create_meeting(
        db=db,
        file=file,
        title=title,
        user=current_user,
    )

 

@router.get("")
def get_my_meetings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):

    meetings = get_user_meetings(
        db=db,
        user_id=current_user.id,
    )


    return [
        {
            "id": meeting.id,
            "title": meeting.title,
            "created_at": meeting.created_at,
        }
        for meeting in meetings
    ]


@router.get("/{meeting_id}")
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):

    meeting = get_meeting_by_id(
        db=db,
        meeting_id=meeting_id,
        user_id=current_user.id,
    )

    owner_id = get_meeting_owner(db,meeting.id).id

    return {

        "id": meeting.id,

        "title": meeting.title,

        "created_at": meeting.created_at,

        "transcripts": meeting.transcript,

        "summary": meeting.summary,


        "is_owner": owner_id == current_user.id ,


        "audio": {

            "id": meeting.audio.id,

            "path": meeting.audio.path

        }
        if meeting.audio

        else None

    }

@router.get("/{meeting_id}/audio")
def get_meeting_audio(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):


    meeting = get_meeting_by_id(
        db=db,
        meeting_id=meeting_id,
        user_id=current_user.id,
    )


    if not meeting.audio:

        raise HTTPException(
            status_code=404,
            detail="Audio not found"
        )


    file_path = Path(
        meeting.audio.path
    )


    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file missing"
        )


    return FileResponse(
        path=file_path,
        media_type="audio/webm",
        filename=file_path.name
    )


@router.post("/{meeting_id}/participants")
def add_participant(
    meeting_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):

    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )


    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )



    owner_id = get_meeting_owner(db,meeting.id).id



    if owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only owner can add participants"
        )




    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_verified == True
        )
        .first()
    )



    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found or not verified"
        )




    exists = (
        db.query(MeetingUser)
        .filter(
            MeetingUser.meeting_id == meeting_id,
            MeetingUser.user_id == user_id
        )
        .first()
    )


    if exists:
        raise HTTPException(
            status_code=400,
            detail="User already added"
        )




    participant = MeetingUser(
        meeting_id=meeting_id,
        user_id=user_id,
        role="participant"
    )


    db.add(participant)

    db.commit()

    db.refresh(participant)



    return {
        "message":"Participant added successfully",
        "user_id":user_id
    }


@router.delete("/{meeting_id}")
def remove_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user),
):


    return delete_meeting(
        db=db,
        meeting_id=meeting_id,
        user_id=current_user.id
    )