from app.services.rag.embedding import create_embeddings
from app.models.chunk import MeetingChunk
from app.core.database import SessionLocal
from app.core.VDB import load_faiss_index



def search_meeting(meeting_id: int,question: str,top_k: int = 5):

    db = SessionLocal()

    try:

        index = load_faiss_index(
            meeting_id
        )

        question_embedding = create_embeddings(
            [question]
        )

        question_embedding = (
            question_embedding
            .astype("float32")
        )

        scores, indices = index.search(
            question_embedding,
            top_k
        )


        chunk_indexes = indices[0]

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

        
        results = []


        for idx, score in zip(
            chunk_indexes,
            scores[0]
        ):

            if idx == -1:
                continue


            chunk = chunks[idx]


            results.append(
                {
                    "text": chunk.content,
                    "start": chunk.start_time,
                    "end": chunk.end_time,
                    "score": float(score),
                }
            )


        return results


    finally:

        db.close()