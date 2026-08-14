from fastapi import HTTPException
import json
import re
import httpx
from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.models.segment import Segment
from app.core.model_tokenier import tokenizer
from app.schemas import meeting
OLLAMA_URL = "http://localhost:11434/api/chat"


system_prompt_text = """
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
        "text":"(النص كما هو)"
      }
    ]
   """ 
def calculate_params(transcript: str, system_prompt: str, estimated_segments: int = 10):
    input_tokens = len(tokenizer.encode(system_prompt + transcript))
    
    json_overhead = estimated_segments * 20
    
    estimated_output = input_tokens + json_overhead
    
    num_predict = int(estimated_output * 1.3)
    num_ctx = int((input_tokens + num_predict) * 1.15)  # extra headroom
    
    def round_ctx(n):
        for step in [512,1024,2048, 4096, 8192, 16384, 32768]:
            if n <= step:
                return step
        return 32768  # Qwen2.5 practical ceiling without special rope scaling
    
    return num_predict, round_ctx(num_ctx)

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
    num_predict, num_ctx = calculate_params(meeting.transcript, system_prompt_text)
    payload = {
        "model": "segment-model",
        "stream": False,
        "messages": [
            {
            "role": "system",
            "content": system_prompt_text
        },
        {
            "role":"user",
            "content": meeting.transcript
            }
        ],
    "options": {
        "temperature": 0,
        "num_predict": num_predict,
        "num_ctx": num_ctx,
        "num_gpu": 1,
        "num_thread": 4
    }
    }


    async with httpx.AsyncClient(timeout=1000) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )


    response.raise_for_status()

    result = response.json()

    model_output = result["message"]["content"]

    # print("Model Output:", model_output)  # Debugging line
    try:
        segments_data = json.loads(model_output)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Model did not return valid JSON"
        )

    # print("Segments Data:", segments_data)  # Debugging line
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
    num_predict, num_ctx = calculate_params(segment.segment, "أنت خبير في تلخيص الاجتماعات واستخراج القرارات.", estimated_segments=1)
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
                "content": f"لخص واستخرج كل القرارات الواردة في الاجتماع : {segment.segment}"
            }
        ],
        "options": {
            "temperature": 0,
            "num_predict": num_predict,
            "num_ctx": num_ctx,
            "num_gpu": 1,
            "num_thread": 4
        }
    }

    async with httpx.AsyncClient(timeout=1000) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

    response.raise_for_status()

    result = response.json()

    output = result["message"]["content"]
    # print("Model Output:", output)  # Debugging line
    summary_match = re.search(r"الملخص\s*:\s*(.*?)(?=\s*\|\s*القرارات\s*:|$)",output,re.DOTALL)

    decisions_match = re.search(r"القرارات\s*:\s*(.*)$",output,re.DOTALL)
    # print("decisions_match:", decisions_match.group(1) if decisions_match else "No match")  # Debugging line
    segment.summary = summary_match.group(1).strip() if summary_match else ""
    segment.decisions = decisions_match.group(1).strip() if decisions_match else ""
    db.commit()

    return {
        "segment_id": segment.id,
        "summary": segment.summary,
        "decisions": segment.decisions
    }