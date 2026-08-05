from app.ai.model_manager import model_manager
from app.core.Enum import TranscriptStatus
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.meeting import Meeting
from app.models.chunk import MeetingChunk
from app.core.VDB import build_faiss_index, save_faiss_index



def run_embedding_pipeline(meeting_id: int):

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


        if not meeting or meeting.embedding_status == TranscriptStatus.COMPLETED:
            return


        meeting.embedding_status = TranscriptStatus.PROCESSING

        db.commit()


        chunks = (
            db.query(MeetingChunk)
            .filter(
                MeetingChunk.meeting_id == meeting_id
            )
            .order_by(
                MeetingChunk.chunk_index
            )
            .all()
        )


        if not chunks:
            raise Exception(
                "No chunks found for meeting"
            )


        texts = [
            chunk.content
            for chunk in chunks
        ]


        embeddings = create_embeddings(texts)

        
        index = build_faiss_index(embeddings)

        save_faiss_index(meeting.id,index)


        meeting.embedding_status = TranscriptStatus.COMPLETED

        db.commit()



    except Exception as e:


        print(
            "Embedding error:",
            e
        )


        if meeting:

            meeting.embedding_status = TranscriptStatus.FAILED

            db.commit()



    finally:

        db.close()

def create_embeddings(texts: list[str]):

    model = model_manager.embedding_model

    if model is None:
        raise RuntimeError(
            "Embedding model is not loaded."
        )

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return embeddings


