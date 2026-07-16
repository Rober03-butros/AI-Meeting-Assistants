from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.services.auth import register_user
from app.core.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/register',response_model=UserResponse,status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)
