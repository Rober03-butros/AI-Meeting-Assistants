from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.dependencies import security

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import LogoutRequest, RefreshTokenRequest, TokenResponse
from app.schemas.verification import ResendVerificationRequest, VerifyEmailRequest
from app.services.auth import login_user, logout_user, refresh_access_token, register_user
from app.core.database import get_db
from fastapi import BackgroundTasks
from app.services.email import send_verification_email
from app.services.verification import resend_verification_code, verify_email_code


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/register',response_model=UserResponse,status_code=201)
def register(user_data: UserCreate,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    user, verification = register_user(
        db=db,
        user_data=user_data,
    )

    background_tasks.add_task(
        send_verification_email,
        user.email,
        verification.code,
    )
    return user

@router.post('/login',response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)

@router.post("/refresh")
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db,refresh_data)

@router.post("/logout")
def logout(
    logout_data: LogoutRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return logout_user(
        db=db,
        access_token=credentials.credentials,
        refresh_token=logout_data.refresh_token,
    )

@router.post("/verify-email")
def verify_email(
    data: VerifyEmailRequest,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    verify_email_code(
        db=db,
        user=user,
        code=data.code,
    )

    return {
        "message": "Email verified successfully."
    }

@router.post("/resend-verification")
def resend_verification(
    data: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    verification = resend_verification_code(
        db=db,
        email=data.email,
    )

    background_tasks.add_task(
        send_verification_email,
        data.email,
        verification.code,
    )

    return {
        "message": "Verification code sent successfully."
    }


@router.get("/me",response_model=UserResponse,)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
