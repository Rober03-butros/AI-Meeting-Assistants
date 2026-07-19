from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.verification import router as verification_router
from app.api.meeting import router as meeting_router
from app.api.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

