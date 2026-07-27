from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.meeting import Meeting
from app.core.Enum import TranscriptStatus

from app.ai.model_manager import model_manager


def run_transcription(meeting_id: int):

    db: Session = SessionLocal()

    meeting = None


    try:


        meeting = ( 
            db.query(Meeting)
            .filter(
                Meeting.id == meeting_id
            )
            .first()
        )


        if not meeting:
            return



        meeting.transcript_status = TranscriptStatus.PROCESSING

        db.commit()


        audio_path = meeting.audio.path

        
        whisper = model_manager.whisper
        
        
        if whisper is None:

            raise Exception(
                "Whisper model is not loaded"
            )

        result = whisper["pipeline"](
            audio_path,
            return_timestamps=True,
            generate_kwargs={
            "language": "ar",
            "task": "transcribe",
            },
        )


        meeting.transcript = result['text']


        meeting.transcript_status = "COMPLETED"



        db.commit()



    except Exception as e:

        print(
            
            "Transcription error:",
            e
        )


        if meeting:

            meeting.transcript_status = "FAILED"

            db.commit()



    finally:

        db.close()

