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



# app = FastAPI()


# segments = [

#     {
#         "start": 0.0,
#         "end": 5.0,
#         "text": "Good morning everyone. Welcome to today's meeting."
#     },

#     {
#         "start": 5.0,
#         "end": 10.0,
#         "text": "Today we will discuss the progress of the AI Meeting Assistant project."
#     },

#     {
#         "start": 10.0,
#         "end": 15.0,
#         "text": "The speech recognition model has already been integrated successfully."
#     },

#     {
#         "start": 15.0,
#         "end": 20.0,
#         "text": "The next task is building the Retrieval Augmented Generation pipeline."
#     },

#     {
#         "start": 20.0,
#         "end": 25.0,
#         "text": "We also need to store vector embeddings for every meeting chunk."
#     },

#     {
#         "start": 25.0,
#         "end": 30.0,
#         "text": "FAISS was selected because each meeting will have its own vector index."
#     },

#     {
#         "start": 30.0,
#         "end": 35.0,
#         "text": "Users will only search inside the current meeting instead of all meetings."
#     },

#     {
#         "start": 35.0,
#         "end": 40.0,
#         "text": "Finally we should implement conversational retrieval using previous chat history."
#     }

# ]

# chunks = create_chunks(segments,max_words=20, min_words=10, overlap_ratio=0.2)

# @app.get("/")
# def upload_meeting_audio(
#     db: Session = Depends(get_db)
# ):

#     save_chunks(db, meeting_id=15, chunks=chunks)
#     return 'chunks saved successfully'

# @app.get('/test')
# def test_embedding():
#     answer = generate_answer(meeting_id=15, question="What are the next tasks after integrating the speech recognition model?")
#     return {
#         'question': "What are the next tasks after integrating the speech recognition model?",
#         'answer': answer
#     }
    # return search_meeting(15,"why we select FAISS")
#     run_embedding_pipeline(meeting_id=15)


# # print("Generated Chunks:")
# # for c in chunks:
# #     print(f"Start: {c.start}, End: {c.end}, Text: {c.text}")

