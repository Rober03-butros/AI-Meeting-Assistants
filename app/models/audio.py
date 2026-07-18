from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Audio(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    path: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )