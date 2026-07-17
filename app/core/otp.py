import secrets
from datetime import datetime, timedelta, timezone

OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 10


def generate_otp() -> str:
    return "".join(
        str(secrets.randbelow(10))
        for _ in range(OTP_LENGTH)
    )


def otp_expiration() -> datetime:
    return datetime.now(timezone.utc) + timedelta(
        minutes=OTP_EXPIRE_MINUTES
    )