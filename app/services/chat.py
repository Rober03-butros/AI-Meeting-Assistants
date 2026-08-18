from app.models.chat_messages import ChatMessage
from app.models.user import User
from app.schemas.chatschema import ChatHistoryResponse, ChatMessageResponse
from app.services.meeting_services import get_meeting_by_id
from app.ai.gemini import generate_answer
from app.services.rag.reranker import rerank_chunks
from app.services.rag.retrieval import search_meeting
from sqlalchemy.orm import Session
from app.services.rag.query_rewrite import rewrite_question


def ask(db: Session,meeting_id: int,user_id: int,question: str):

    history = get_conversation_history(
        db=db,
        meeting_id=meeting_id,
        user_id=user_id,
    )

    conversation_history = build_conversation_history(history)

    rewritten_question = rewrite_question(question,conversation_history)

    chunks = search_meeting(
          meeting_id=meeting_id,
          question=rewritten_question,
          top_k=15
      )
  
  
    chunks = rerank_chunks(
          query=rewritten_question,
          retrieved_chunks=chunks,
          k=8
      )

    chunks = [x for x in chunks if x['rerank_score'] >= 0.0013]
    
  
    if len(chunks) == 0:
  
        return {
            "answer": 'لم يتم ذكر مثل هذه المعلومة في الاجتماع.',
            "sources": [],
        }


    result = generate_answer(
        chunks=chunks,
        question=rewritten_question,
    )

    if result["answer"] == 'لم يتم ذكر مثل هذه المعلومة في الاجتماع.':

        return {
            "answer": result["answer"],
            "sources": [],
        }
  
  
    chat = ChatMessage(
        meeting_id=meeting_id,
        user_id=user_id,
        question=question,
        rewritten_question = rewritten_question,
        answer = result["answer"],
        sources = result["sources"]
    )
          
    db.add(chat)
    db.commit()
  
  
    return {
        "answer": chat.answer,
        "sources": chat.sources,
    }


def chat_history(db: Session, meeting_id: int, current_user: User,limit: int | None = None):
    meeting = get_meeting_by_id(
        db=db,
        meeting_id=meeting_id,
        user_id=current_user.id,
    )

    query = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.meeting_id == meeting.id,
            ChatMessage.user_id == current_user.id,
        )
        .order_by(ChatMessage.created_at.desc())
    )

    if limit is not None:
        query = query.limit(limit)

    messages = query.all()

    return ChatHistoryResponse(
        messages=[
            ChatMessageResponse(
                id=message.id,
                question=message.question,
                answer=message.answer,
                sources=message.sources or [],
                created_at=message.created_at,
            )
            for message in messages
        ]
    )

def get_conversation_history(db: Session,meeting_id: int,user_id: int,limit: int = 3):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.meeting_id == meeting_id,
            ChatMessage.user_id == user_id,
        )
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )

    return messages

def build_conversation_history(messages: list[ChatMessage]):

    if not messages:
        return ""

    history = []

    for message in messages:

        history.append(
            f"User: {message.question}"
        )

        if message.answer:
            history.append(
                f"Assistant: {message.answer}"
            )

    return "\n".join(history)