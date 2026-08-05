from fastapi import APIRouter,HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.segment import Segment
from app.core.dependencies import get_verified_user
from app.core.database import get_db
from app.services.segment_services import segment_function

router = APIRouter(
    prefix="/segment",
    tags=["segment"],
    dependencies=[Depends(get_verified_user)]
) 
@router.post("/segment/{meeting_id}")
async def segment_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
):

    return await segment_function(meeting_id=meeting_id, db=db)


@router.get("/get_segment/{segment_id}")
def get_segment(
    segment_id: int,
    db: Session = Depends(get_db),
):
    segment = db.query(Segment).filter(Segment.id == segment_id).first()

    if not segment:
        raise HTTPException(
            status_code=404,
            detail="Segment not found",
        )

    return {
        "id": segment.id,
        "meeting_id": segment.meeting_id,
        "title": segment.title,
        "segment": segment.segment,
        "summary": segment.summary,
        "decisions": segment.decisions,
        "start_time": segment.start_time,
        "end_time": segment.end_time
    }


@router.get("/get_all_segments/{meeting_id}")
def get_all_segments(meeting_id: int ,session: Session = Depends(get_db)):
    segments = session.query(Segment).filter(Segment.meeting_id == meeting_id).all()

    if not segments:
        raise HTTPException(
            status_code=404,
            detail="No segments found for this meeting",
        )
    segments = sorted(segments, key=lambda x: x.id)
    return [
        {
            "id": segment.id,
            "meeting_id": segment.meeting_id,
            "title": segment.title,
            "segment": segment.segment,
            "summary": segment.summary,
            "decisions": segment.decisions,
            "start_time": segment.start_time,
            "end_time": segment.end_time
        }
        for segment in segments
    ]
