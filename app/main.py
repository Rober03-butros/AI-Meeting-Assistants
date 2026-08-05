from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.verification import router as verification_router
from app.api.meeting import router as meeting_router
from app.api.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.ai.model_manager import model_manager



app = FastAPI()

@app.on_event("startup")
def startup_event():
    
    print("Starting server...")

    model_manager.load_models()

    print("Server ready.")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(verification_router)
app.include_router(meeting_router)
app.include_router(user_router)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# =================================== for testing ===================================
# from app.core.dependencies import get_db
# from app.services.rag.chunk import create_chunks,save_chunks
# from fastapi import Depends, FastAPI
# from sqlalchemy.orm import Session
# from app.services.rag.embedding import create_embeddings, run_embedding_pipeline
# from app.services.rag.generation import generate_answer
# from app.core.config import Settings
# from app.services.rag.retrieval import search_meeting
# from app.services.rag.reranker import rerank_chunks


# # app = FastAPI()

# segments = [
# {
#     "start": 0.0,
#     "end": 30.0,
#     "text": "أحمد: صباح الخير يا جماعة، كيفكم؟ خلونا نبدأ اجتماع اليوم. عندنا كم نقطة بدنا نراجعها بخصوص مشروع AI Meeting Assistant، نشوف شو خلصنا خلال الأسبوع الماضي، وإيش الأشياء اللي لسه معلقة، ونرتب أولوياتنا للفترة الجاية."
# },

# {
#     "start": 30.0,
#     "end": 60.0,
#     "text": "سارة: بالنسبة للـ backend، إحنا قطعنا شوط كبير. خلصنا أغلب الـ APIs باستخدام Laravel، وصار المستخدم يقدر يعمل create meeting ويشوف الاجتماعات القديمة ويعدل عليها. عملنا كمان testing للـ endpoints وما طلع معنا مشاكل كبيرة."
# },

# {
#     "start": 60.0,
#     "end": 90.0,
#     "text": "محمد: من ناحية الـ frontend، اشتغلنا على React مع JavaScript. خلصنا صفحة الـ login، وصفحة عرض الاجتماعات، وكمان جزء المحادثة مع الـ AI. باقي علينا شوية تحسينات بالـ UI وترتيب بعض التفاصيل الصغيرة."
# },

# {
#     "start": 90.0,
#     "end": 120.0,
#     "text": "أحمد: تمام، طيب بالنسبة للتسجيلات الصوتية؟ هل خلصنا موضوع تحويل الصوت إلى نص ولا لسه في مشاكل؟"
# },

# {
#     "start": 120.0,
#     "end": 150.0,
#     "text": "سارة: لا، خلصنا دمج Whisper. بصراحة النتائج كانت جيدة، خصوصًا لما يكون الصوت واضح. المشكلة الوحيدة إنه لما يكون في أكثر من شخص يحكي بنفس الوقت أو يكون في إزعاج بالخلفية، النص أحيانًا يطلع فيه أخطاء."
# },

# {
#     "start": 150.0,
#     "end": 180.0,
#     "text": "محمد: بعد ما يطلع النص، إحنا بنعمل له تقسيم إلى Chunks. كل جزء بنطلع له Embedding وبعدين نخزنهم داخل FAISS. الفكرة إنه لما المستخدم يسأل سؤال ما نبحث في كل شيء، نبحث بس داخل الاجتماع المطلوب."
# },

# {
#     "start": 180.0,
#     "end": 210.0,
#     "text": "أحمد: بس خلينا نتأكد من نقطة الـ Vector Index. إحنا ما زلنا عاملين Index منفصل لكل Meeting صح؟ يعني ما دمجنا كل الاجتماعات مع بعض؟"
# },

# {
#     "start": 210.0,
#     "end": 240.0,
#     "text": "محمد: نعم بالضبط، كل اجتماع إله Vector Index خاص فيه. جربنا الطريقة الثانية قبل، بس كانت النتائج أقل دقة لأنه أحيانًا يجيب معلومات من اجتماع ثاني ما إلها علاقة بالسؤال."
# },

# {

#     "start": 240.0,
#     "end": 270.0,
#     "text": "سارة: كمان اشتغلنا على موضوع Conversational RAG. يعني لو المستخدم سأل سؤال مثل 'طيب وماذا عن قاعدة البيانات؟' النظام يفهم إنه يقصد نفس المشروع اللي كنا نحكي عنه قبل، ويعمل Query Rewrite قبل عملية البحث."
# },

# {
#     "start": 270.0,
#     "end": 300.0,
#     "text": "أحمد: هذا الجزء مهم جدًا، لأنه المستخدم غالبًا ما رح يعيد السؤال كامل كل مرة. هو متوقع النظام يفهم سياق المحادثة زي أي Chat Assistant."
# },

# {
#     "start": 300.0,
#     "end": 330.0,
#     "text": "محمد: بالنسبة للـ Llama، عدلنا الـ Prompt شوي. خليناه يعتمد فقط على النص اللي نرجعه من الـ RAG، وما يعطي معلومات من عنده. إذا المعلومة مش موجودة يقول إنه ما لقاها بدل ما يخمن."
# },

# {
#     "start": 330.0,
#     "end": 360.0,
#     "text": "سارة: لاحظنا كمان إنه بعض الأسئلة تحتاج أكثر من Chunk عشان يطلع جواب كامل. لذلك غيرنا الـ retrieval وخليّنا النظام يرجع أكثر من جزء مرتبط بالسؤال قبل ما يبعثهم للـ Llama."
# },

# {
#     "start": 360.0,
#     "end": 390.0,
#     "text": "أحمد: طيب بالنسبة لقاعدة البيانات، شو قررنا بالنهاية؟ هل نكمل على PostgreSQL ولا في خيار ثاني؟"
# },

# {
#     "start": 390.0,
#     "end": 420.0,
#     "text": "سارة: لا، قررنا نكمل على PostgreSQL. نخزن فيها بيانات المستخدمين والاجتماعات، أما ملفات الصوت نفسها فنحطها في Object Storage عشان ما يصير عندنا ضغط على قاعدة البيانات."
# },

# {
#     "start": 420.0,
#     "end": 450.0,
#     "text": "محمد: أضفت كمان Metadata لكل Chunk. يعني نخزن وقت بداية ونهاية الجزء، واسم الشخص اللي حكى، ورقم الاجتماع. هذا بيساعدنا لما المستخدم يضغط على الإجابة ويرجع يسمع الجزء الأصلي من التسجيل."
# },

# {
#     "start": 450.0,
#     "end": 480.0,
#     "text": "أحمد: ممتاز. لازم كمان نضيف Logging عشان نعرف وين المشكلة لو صار في بطء. بدنا نشوف وقت الـ Query Rewrite، ووقت البحث في FAISS، ووقت رد الـ Llama."
# },

# {
#     "start": 480.0,
#     "end": 510.0,
#     "text": "سارة: أنا الأسبوع الجاي رح أركز على تحسين واجهة المستخدم. بدي أضيف صفحة تعرض الـ transcript كامل، ويكون فيه إمكانية تضغط على أي جزء وتروح مباشرة للوقت الموجود في التسجيل."
# },

# {
#     "start": 510.0,
#     "end": 540.0,
#     "text": "محمد: وأنا رح أكمل على تحسين الـ Embeddings. رح أجرب أكثر من model ونقارن النتائج، لأنه جودة البحث تعتمد كثير على اختيار الـ embedding model المناسب."
# },

# {
#     "start": 540.0,
#     "end": 570.0,
#     "text": "أحمد: تمام يا جماعة، هيك نكون خلصنا. خلونا نلتزم بالمهام اللي اتفقنا عليها، وبالاجتماع الجاي نشوف النتائج ونقارن الأداء. يعطيكم العافية جميعًا."
# }
# ]

# chunks = create_chunks(segments,60,10)

# @app.get("/")
# def upload_meeting_audio(
#     db: Session = Depends(get_db)
# ):
#     save_chunks(db, meeting_id=17, chunks=chunks)
#     run_embedding_pipeline(meeting_id=17)
#     return f'number of chunks is {len(chunks)}chunks saved successfully'

# @app.get('/test')
# def test_embedding():
#     question = "Why we use FIASS?"
# #     answer = generate_answer(meeting_id=15, question=question)
# #     return {
# #         'question': question,
# #         'answer': answer
# #     }
#     without_reranker =  search_meeting(15,question)
#     with_reranker = rerank_chunks(
#         query=question,
#         retrieved_chunks=without_reranker,
#         k=3
#     )
#     return {
#         'without_reranker': without_reranker,
#         'with_reranker': with_reranker
#     }
    # run_embedding_pipeline(meeting_id=15)


# print("Generated Chunks:")
# for c in chunks:
#     print(f"Start: {c.start}, End: {c.end}, Text: {c.text}")

