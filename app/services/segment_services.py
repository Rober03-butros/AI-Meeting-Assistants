from fastapi import HTTPException
import json
import re
import httpx
from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.models.segment import Segment

OLLAMA_URL = "http://localhost:11434/api/chat"

def clean_text(text: str) -> str:
    print("NEW clean_text() called")

    pattern = r'"text":\s*"(?P<text>[^"]*)",\s*"speaker":\s*"(?P<speaker>S\d+)"'

    matches = re.finditer(pattern, text)

    extracted_data = []

    for match in matches:
        dialogue = match.group("text")
        speaker = match.group("speaker").replace("S", "speaker")

        extracted_data.append({speaker: dialogue})

    concatenated_dialogue = ""

    for item in extracted_data:
        speaker = next(iter(item))
        concatenated_dialogue += f"{speaker}: {item[speaker]}\n"

    return concatenated_dialogue

async def segment_function(meeting_id: int, db: Session):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    if not meeting.transcript:
        raise HTTPException(
            status_code=400,
            detail="Meeting has no transcript"
        )
    if db.query(Segment).filter(Segment.meeting_id == meeting.id).first():
        raise HTTPException(
            status_code=400,
            detail="Segments already exist for this meeting"
        )
    Cleaned_Transcript = clean_text(meeting.transcript)
    # print("Cleaned Transcript:", meeting.transcript)  # Debugging line
    payload = {
        "model": "qwen3b-f16",
        "stream": False,
        "messages": [
            {
            "role": "system",
            "content": """
    أنت خبير في تقسيم نصوص الاجتماعات.

    مهمتك هي تقسيم النص إلى مقاطع (Topic Segments) فقط.
    كل عنصر في text يجب أن يحتوي على الأسطر الأصلية كما هي تمامًا.

    لا تحذف أسماء المتحدثين.

    لا تحذف أي رمز.

    لا تغير علامات الترقيم.

    لا تدمج الجمل.

    لا تعدل ترتيب الأسطر.

    يجب أن يكون كل سطر في المخرجات مطابقًا للسطر الموجود في الإدخال.
    القواعد:
    0. افهم النص المكتوب جيداً أولاً
    1. لا تلخص النص.
    2. لا تحذف أي كلمة.
    3. لا تضف أي كلمة.
    4. لا تعيد صياغة الجمل.
    5. إذا كان الموضوع تمت إعادة الحديث عنه في جمل بعدها أعد جمعها مع الفكرة التي تناسبها.
    6. لا تجعل هناك تداخل بين المواضيع أجعل كل موضوع ضمن الفكرة الخاصة به فقط
    7. لا تضع علامات ترقيم
    8. احتفظ بالنص كما هو حرفياً.
    9. كل مقطع يمثل فكرة أو موضوعاً واحداً.
    10. إذا انتقل الحديث إلى فكرة جديدة ابدأ Topic جديد.
    11. أعد النتيجة بصيغة JSON فقط.

        الصيغة المطلوبة:

    [
      {
        "topic":"عنوان قصير",
        "text":"speaker1: (النص كما هو)
        speaker2: (النص كما هو)
        ..."
      }
    ]
    """
        },
        {
            "role":"user",
            "content": Cleaned_Transcript
            }
        ]
    }


    async with httpx.AsyncClient(timeout=1000) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )


    response.raise_for_status()

    result = response.json()

    model_output = result["message"]["content"]


    try:
        segments_data = json.loads(model_output)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Model did not return valid JSON"
        )

    print("Segments Data:", segments_data)  # Debugging line
    # Save segments
    db.query(Segment).filter(Segment.meeting_id == meeting.id).delete()
    db.commit()
    merged = {}

    for item in segments_data:
        topic = re.sub(
            r"\s*(?:متابعة|continued|cont\.?|more)\s*$",
            "",
            item["topic"],
            flags=re.IGNORECASE,
        ).strip()

        if topic in merged:
            merged[topic]["text"] += "\n" + item["text"]
        else:
            merged[topic] = {
                "topic": topic,
                "text": item["text"],
            }

    segments_data = list(merged.values())
    for item in segments_data:

        segment = Segment(
            meeting_id=meeting.id,
            title=item.get("topic", ""),
            segment=item.get("text", ""),
            summary=None,
            decisions=None,
            start_time=0,
            end_time=0
        )

        db.add(segment)


    db.commit()


    return {
        "meeting_id": meeting.id,
        "segments_created": len(segments_data),
        "segments_data": segments_data
    }



async def summarize_segment(segment_id: int, db: Session):
    segment = (
        db.query(Segment)
        .filter(Segment.id == segment_id)
        .first()
    )

    if segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")

    if not segment.segment:
        raise HTTPException(status_code=400, detail="Segment has no content")
    if segment.summary is not None and segment.decisions is not None:
        raise HTTPException(
            status_code=400,
            detail="Segment is already summarized"
        )
    payload = {
        "model": "syrian-summary",
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": "أنت خبير في تلخيص الاجتماعات واستخراج القرارات."
            },
            {
                "role": "user",
                "content": f"لخص واستخرج القرارات : {segment.segment}"
            }
        ]
    }

    async with httpx.AsyncClient(timeout=1000) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

    response.raise_for_status()

    result = response.json()

    output = result["message"]["content"]
    summary_match = re.search(r"الملخص\s*:\s*(.*?)(?=\s*\|\s*القرارات\s*:|$)",output,re.DOTALL)

    decisions_match = re.search(r"القرارات\s*:\s*(.*)$",output,re.DOTALL)

    segment.summary = summary_match.group(1).strip() if summary_match else ""
    segment.decisions = decisions_match.group(1).strip() if decisions_match else ""
    db.commit()

    return {
        "segment_id": segment.id,
        "summary": segment.summary,
        "decisions": segment.decisions
    }