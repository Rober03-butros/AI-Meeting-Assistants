from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.meeting import Meeting
import shutil

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



        meeting.transcript_status = "PROCESSING"

        db.commit()

        whisper = model_manager.whisper


        if whisper is None:

            raise Exception(
                "Whisper model is not loaded"
            )


        # model = whisper["model"]

        # processor = whisper["processor"]


        audio_path = meeting.audio.path


        # result = model.transcribe(
        #     audio_path
        # )


        result = whisper(audio_path, return_timestamps=True)
        # rag_data = {
        #     "full_text": result["text"],
        #     "segments": result["chunks"]
        # }
        # result = transcribe_for_rag(audio_path)


        transcript = ""



        # for segment in result["segments"]:

        #     transcript += (
        #         segment["text"]
        #         + "\n"
        #     )


        meeting.transcript = result["text"]


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

