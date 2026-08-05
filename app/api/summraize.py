
from fastapi import APIRouter, File, Form, HTTPException
from fastapi import APIRouter, Depends
import httpx
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.meeting import Meeting
from app.models.segment import Segment
from app.models.user import User
from app.schemas.meeting import Meeting_transcript_Response, MeetingResponse, Meetings_Response
from app.core.dependencies import get_verified_user
from app.core.database import get_db
from app.services.meeting_services import add_transcript_to_meeting
from app.services.segment_services import clean_text, segment_function, summarize_segment



router = APIRouter(
    prefix="/summarize",
    tags=["summarize"],
    dependencies=[Depends(get_verified_user)]
)






@router.post("/summarize/{segment_id}")
async def summarize_meeting(
    segment_id: int,
    db: Session = Depends(get_db),
):
    if not segment_id:
        raise HTTPException(
            status_code=400,
            detail="Segment ID is required",
        )
    
    return await summarize_segment(segment_id=segment_id, db=db)




@router.post("/summarize_all/{meeting_id}")
async def summarize_all_segments(
    meeting_id: int,
    db: Session = Depends(get_db),
):
    segments = db.query(Segment).filter(Segment.meeting_id == meeting_id).all()

    if not segments:
        raise HTTPException(
            status_code=404,
            detail="No segments found for this meeting",
        )

    results = []
    for segment in segments:
        if segment.summary is not None and segment.decisions is not None:
            results.append({
                "segment_id": segment.id,
                "summary": segment.summary,
                "decisions": segment.decisions
            })
        else:
            result = await summarize_segment(segment.id, db)
            results.append(result)

    return {
        "meeting_id": meeting_id,
        "summarized_segments": results
    }


@router.get("/get_summarized_segments/{meeting_id}")
def get_summarized_segments(meeting_id: int,db: Session = Depends(get_db)):
    segments = db.query(Segment).filter(Segment.meeting_id == meeting_id).all()

    if not segments:
        raise HTTPException(
            status_code=404,
            detail="No segments found for this meeting",
        )


    summarized_segments = [
        {
            "segment_id": segment.id,
            "summary": segment.summary,
            "decisions": segment.decisions
        }
        for segment in segments if segment.summary is not None and segment.decisions is not None
    ]

    if not summarized_segments:
        raise HTTPException(
            status_code=404,
            detail="No summarized segments found for this meeting",
        )

    return {
        "meeting_id": meeting_id,
        "summarized_segments": summarized_segments
    }

