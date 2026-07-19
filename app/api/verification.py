from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import security

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.verification import ResendVerificationRequest, VerifyEmailRequest
from app.core.database import get_db
from fastapi import BackgroundTasks
from app.services.email import send_verification_email
from app.services.verification import resend_verification_code, verify_email_code


router = APIRouter(
    prefix="/verify",
    tags=["verification"]
)



@router.post("/verify-email")
def verify_email(data: VerifyEmailRequest,db: Session = Depends(get_db)):

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