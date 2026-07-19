import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.meeting import Meeting
from app.models.audio import Audio
from app.models.meeting_user import MeetingUser
from app.models.user import User
from app.services.audio_services import save_audio_file, upload_audio
from fastapi import HTTPException, status
from app.models.meeting_user import MeetingUser




def create_meeting(db: Session,file: UploadFile,title: str,user: User):

    audio = upload_audio(db,file)

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


def get_user_meetings(db: Session,user_id: int):

    meetings = (
        db.query(Meeting)
        .join(MeetingUser)
        .filter(
            MeetingUser.user_id == user_id
        )
        .all()
    )


    return meetings


def get_meeting_by_id(db: Session,meeting_id: int,user_id: int,):

    meeting = (
        db.query(Meeting)
        .join(MeetingUser)
        .filter(
            Meeting.id == meeting_id,
            MeetingUser.user_id == user_id
        )
        .first()
    )


    if not meeting:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found or access denied."
        )


    return meeting

def get_meeting_owner(db: Session, meeting_id: int) -> User:


    meeting_owner = (
        db.query(User)
        .join(
            MeetingUser,
            MeetingUser.user_id == User.id
        )
        .filter(
            MeetingUser.meeting_id == meeting_id,
            MeetingUser.role == "owner",
        )
        .first()
    )

    if meeting_owner is None:
        raise HTTPException(
            status_code=500,
            detail="Meeting has no owner."
        )

    return meeting_owner



def delete_meeting(db: Session,meeting_id: int,user_id: int):

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



    owner = get_meeting_owner(db, meeting_id)



    if owner.id != user_id:

        raise HTTPException(
            status_code=403,
            detail="Only owner can delete meeting"
        )


    if meeting.audio:

        file_path = meeting.audio.path


        if os.path.exists(file_path):

            os.remove(file_path)



    db.query(MeetingUser).filter(
            MeetingUser.meeting_id == meeting_id
        ).delete()


    if meeting.audio:

        db.delete(
            meeting.audio
        )

    db.delete(
        meeting
    )

    db.commit()

    return {
        "message":
        "Meeting deleted successfully"
    }

