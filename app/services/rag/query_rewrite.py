from app.ai.llama import generate


SYSTEM_PROMPT = """
أنت نظام مسؤول عن إعادة صياغة أسئلة المستخدم فقط.

مهمتك هي تحويل السؤال إلى سؤال واضح يصلح للبحث داخل نظام RAG.

القواعد:

- لا تجب على السؤال.
- لا تشرح.
- لا تضف أي تعليق.
- لا تقل "السؤال الجديد هو".
- إذا كان السؤال واضحًا أصلًا فأعده كما هو.
- إذا كان السؤال يعتمد على المحادثة السابقة، فأعد كتابته ليصبح مستقلاً.
- أعد السؤال فقط ولا تكتب أي شيء آخر.
"""


def rewrite_question(
    question: str,
    conversation_history: str,
):

    prompt = f"""
المحادثة السابقة:

{conversation_history}

السؤال الحالي:

{question}

أعد كتابة السؤال ليصبح مستقلاً وواضحًا.
"""

    return generate(
        prompt=prompt,
        system=SYSTEM_PROMPT,
        temperature=0,
    )