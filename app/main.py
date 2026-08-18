from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.verification import router as verification_router
from app.api.meeting import router as meeting_router
from app.api.user import router as user_router
from app.api.summraize import router as summarize_router
from app.api.segment import router as segment_router
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
app.include_router(user_router)
app.include_router(meeting_router)
app.include_router(segment_router)
app.include_router(summarize_router)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

