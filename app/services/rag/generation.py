from app.ai.llama import generate
from app.models.chat_messages import ChatMessage
from app.services.rag.retrieval import search_meeting
from app.services.rag.reranker import rerank_chunks


SYSTEM_PROMPT = """
You are an AI assistant answering questions about a meeting.

Answer ONLY using the provided meeting transcript.

If the answer does not exist in the transcript, reply:

"I couldn't find this information in the meeting."

Do not invent information.
"""


def build_prompt(question: str,chunks: list[dict]) -> str:

    context = ""

    for i, chunk in enumerate(chunks, start=1):

        context += (
            f"[Chunk {i}]\n"
            f"Time: {chunk['start']} - {chunk['end']} seconds\n"
            f"{chunk['text']}\n\n"
        )


    prompt = f"""
{SYSTEM_PROMPT}

Meeting Transcript:

{context}

Question:

{question}

Answer:
"""

    return prompt



from sqlalchemy.orm import Session




def generate_answer(
    db: Session,
    meeting_id: int,
    user_id: int,
    question: str,
):

    chat = ChatMessage(
        meeting_id=meeting_id,
        user_id=user_id,
        question=question,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)


    chunks = search_meeting(
        meeting_id=meeting_id,
        question=question,
        top_k=8,
    )


    chunks = rerank_chunks(
        query=question,
        retrieved_chunks=chunks,
        k=3,
    )


    if len(chunks) == 0:

        chat.answer = "No information found."
        chat.sources = []

        db.commit()

        return {
            "answer": chat.answer,
            "sources": chat.sources,
        }


    prompt = build_prompt(
        question,
        chunks,
    )


    answer = generate(
        prompt
    )


    chat.answer = answer

    chat.sources = [
        {
            "start": chunk["start"],
            "end": chunk["end"],
        }
        for chunk in chunks
    ]


    db.commit()


    return {
        "answer": chat.answer,
        "sources": chat.sources,
    }