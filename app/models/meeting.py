from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


if TYPE_CHECKING:
    from app.models.audio import Audio
    from app.models.meeting_user import MeetingUser


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Unknown"
    )

    transcript: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    audio_id: Mapped[int] = mapped_column(
    ForeignKey("audio.id"),
    unique=True,
    nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )



    audio: Mapped["Audio"] = relationship(
        "Audio",
        back_populates="meeting",
        uselist=False
    )


    users: Mapped[list["MeetingUser"]] = relationship(
        "MeetingUser",
        back_populates="meeting",
        cascade="all, delete-orphan",
    )