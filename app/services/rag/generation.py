from app.ai.llama import generate
from app.models.chat_messages import ChatMessage
from app.services.rag.retrieval import search_meeting
from app.services.rag.reranker import rerank_chunks
from sqlalchemy.orm import Session




def build_prompt(question: str,chunks: list[dict]) -> str:

    context = ""

    for i, chunk in enumerate(chunks, start=1):

        context += (
            f"{chunk['text']}\n\n"
        )


    prompt =  f"""
        أنت مساعد ذكي متخصص في الإجابة عن أسئلة الاجتماعات.

        ستحصل على أجزاء من نص اجتماع.

        التعليمات:

        - أجب اعتمادًا على النص المرفق فقط.
        - إذا كانت الإجابة موزعة على أكثر من جزء، اجمعها في إجابة واحدة.
        - قدم إجابة واضحة ومفصلة.
        - لا تختصر الإجابة إذا كانت المعلومات موجودة.
        - لا تخترع أي معلومة غير موجودة في النص.
        - إذا لم تكن الإجابة موجودة في النص فقل:
        "لم أجد هذه المعلومة في الاجتماع."

        ====================

        نص الاجتماع:

        {context}

        ====================

        السؤال:

        {question}

        ====================

        الإجابة:
    """

    return prompt



def generate_answer(chunks: list[dict],question: str):

    prompt = build_prompt(
        question,
        chunks,
    )


    answer = generate(
        prompt,
        temperature=0.2
    )

    sources = [
        {
            "start": chunk["start"],
            "end": chunk["end"],
        }
        for chunk in chunks
    ]


    return {
        "answer": answer,
        "sources": sources,
    }