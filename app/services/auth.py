from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import decode_token, hash_password, verify_password
from app.services.token_blacklist import blacklist_token
from app.services.verification import create_email_verification
from app.core.security import verify_password,create_access_token,create_refresh_token
from app.schemas.token import LogoutRequest, RefreshTokenRequest, TokenResponse



def register_user(db: Session, user_data:UserCreate):
    existing_user = (
        db.query(User).filter(User.email == user_data.email).first()
        )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )
    
    hashed_password = hash_password(user_data.password)

    user = User(
        name = user_data.name,
        email = user_data.email,
        hashed_password = hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    verification = create_email_verification(
        db=db,
        user=user,
    )

    return user, verification


def login_user(db: Session,user_data: UserLogin) -> TokenResponse:

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user or not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user.id
    )

    refresh = create_refresh_token(
        user.id
    )

    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh["token"],
        jti=refresh["jti"],
        expires_at=refresh["expires_at"],
    )

    db.add(db_refresh_token)
    db.commit()


    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh["token"],
    )


def refresh_access_token(db: Session,refresh_data: RefreshTokenRequest,):

    try:
        payload = decode_token(
            refresh_data.refresh_token
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )


    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.jti == payload.get("jti")
    ).first()


    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )


    if refresh_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked",
        )


    user_id = int(payload["sub"])


    new_access_token = create_access_token(
        user_id
    )


    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


def logout_user(db: Session,access_token: str,refresh_token: str,):

    try:
        access_payload = decode_token(access_token)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    if access_payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )


    blacklist_token(
        db=db,
        jti=access_payload["jti"],
        exp=access_payload["exp"],
    )


    try:
        refresh_payload = decode_token(refresh_token)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


    if refresh_payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


    refresh = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.jti == refresh_payload["jti"]
        )
        .first()
    )


    if refresh:
        refresh.revoked = True


    db.commit()


    return {
        "message": "Successfully logged out"
    }

