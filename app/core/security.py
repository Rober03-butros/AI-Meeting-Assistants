from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4
from jose import jwt, JWTError

from app.core.config import settings
import bcrypt


BCRYPT_ROUNDS = 12


def hash_password(password: str) -> str:

    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "jti": str(uuid4()),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_refresh_token(user_id: int) -> dict:

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    jti = str(uuid4())

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return {
        "token": token,
        "jti": jti,
        "expires_at": expire,
    }


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc