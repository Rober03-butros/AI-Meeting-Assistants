from sqlalchemy.orm import Session
from app.core.otp import generate_otp, otp_expiration
from app.models.email_verification import EmailVerification
from app.models.user import User
from datetime import datetime, timezone
from fastapi import HTTPException, status


def create_email_verification(
    db: Session,
    user: User,
) -> EmailVerification:

    db.query(EmailVerification).filter(
        EmailVerification.user_id == user.id,
        EmailVerification.used == False,
    ).update(
        {"used": True},
        synchronize_session=False,
    )

    verification = EmailVerification(
        user_id=user.id,
        code=generate_otp(),
        expires_at=otp_expiration(),
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return verification


def verify_email_code(db: Session,user: User,code: str) -> None:

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified.",
        )

    verification = (
        db.query(EmailVerification)
            .filter(
                EmailVerification.user_id == user.id,
                EmailVerification.code == code,
                EmailVerification.used == False,
            )
            .order_by(EmailVerification.created_at.desc())
            .first()
        )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code.",
        )

    if verification.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired.",
        )

    verification.used = True
    user.is_verified = True

    db.commit()


def resend_verification_code(
    db: Session,
    email: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return create_email_verification(
        db=db,
        user=user,
    )