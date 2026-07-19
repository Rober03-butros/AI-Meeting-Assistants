from fastapi import APIRouter, Form

from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_verified_user
from app.models.user import User
from app.core.database import get_db
from app.schemas.meeting import MeetingResponse

from app.schemas.meeting import MeetingResponse
from app.services.meeting_services import create_meeting  


router = APIRouter(
    prefix="/meetings",
    tags=["meetings"]
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




from app.services.meeting_services import get_user_meetings


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