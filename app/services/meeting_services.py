from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.meeting import Meeting
from app.models.audio import Audio
from app.models.meeting_user import MeetingUser
from app.models.user import User
from app.services.audio_services import save_audio_file


def create_meeting(db: Session,file: UploadFile,title: str,user: User):

    path = save_audio_file(file)


    audio = Audio(
        path=path
    )

    db.add(audio)
    db.flush()


    meeting = Meeting(
        audio_id=audio.id,
        title=title
    )

    db.add(meeting)
    db.flush()


    meeting_user = MeetingUser(
        meeting_id=meeting.id,
        user_id=user.id,
        role="owner"
    )

    db.add(meeting_user)


    db.commit()

    db.refresh(meeting)

    return meeting


def get_user_meetings(
    db: Session,
    user_id: int,
):

    meetings = (
        db.query(Meeting)
        .join(MeetingUser)
        .filter(
            MeetingUser.user_id == user_id
        )
        .all()
    )


    return meetings