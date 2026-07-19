from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.token_blacklist import TokenBlacklist


def blacklist_token(db: Session,jti: str,exp: int) -> None:

    exists = (
        db.query(TokenBlacklist)
        .filter(TokenBlacklist.jti == jti)
        .first()
    )

    if exists:
        return

    token = TokenBlacklist(
        jti=jti,
        expires_at=datetime.fromtimestamp(
            exp,
            tz=timezone.utc,
        ),
    )

    db.add(token)


def is_blacklisted(db: Session,jti: str,) -> bool:

    return (
        db.query(TokenBlacklist)
        .filter(TokenBlacklist.jti == jti)
        .first()
        is not None
    )