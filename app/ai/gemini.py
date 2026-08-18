from google import genai
from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def rewrite_query(query: str,history: str):

    prompt = f"""
    أنت نظام يعالج الأسئلة لاستخدامها في البحث ضمن نظام RAG.

    المحادثة السابقة:
    {history}

    السؤال الحالي:
    {query}

    المطلوب:

    1. إذا كان السؤال يعتمد على السياق السابق، أعد صياغته ليصبح مستقلاً.
    2. إذا كان السؤال مستقلاً، أعده كما هو.
    3. إذا كان السؤال طويلاً، قم بتبسيطه مع الحفاظ على معناه.
    4. لا تترجم المصطلح الانكليزي الى العربية ابقيه كما هو
    5. اجعل السؤال:
    - واضحاً
    - مباشراً
    - مناسباً للبحث
    - بدون حشو
    6. لا تضف أي معلومات غير موجودة في السؤال أو المحادثة.
    7. لا تجب عن السؤال.
    8. أعد السؤال المعاد صياغته فقط.

    السؤال المعاد صياغته:
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text.strip()

def generate_answer(chunks: list[dict],question: str):

    context = ""
    
    for i, chunk in enumerate(chunks, start=1):

        context += (
            f"{chunk['text']}\n\n"
        )

    prompt = f"""
    أنت مساعد يجيب عن أسئلة حول اجتماع قد كان موجود ضمنه

    التعليمات:

    - أجب اعتمادًا على النص المرفق فقط.
    - إذا كانت الإجابة موزعة على أكثر من جزء، اجمعها في إجابة واحدة.
    - قدم إجابة واضحة ومفصلة.
    - لا تختصر الإجابة إذا كانت المعلومات موجودة.
    - لا تخترع أي معلومة غير موجودة في النص.
    - إذا لم تكن الإجابة موجودة في النص فقل:
    "لم يتم ذكر مثل هذه المعلومة في الاجتماع."

    محتوى المقال:
    {context}

    السؤال:
    {question}
    أجب اعتماداً على محتوى الاجتماع فقط.
    """
    response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )

    answer = response.text.strip()


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