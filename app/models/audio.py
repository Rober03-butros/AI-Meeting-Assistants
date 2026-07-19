from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.meeting import Meeting


class Audio(Base):

    __tablename__ = "audio"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="audio",
        uselist=False,
    )