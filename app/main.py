from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.audio import router as audio_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(audio_router)

