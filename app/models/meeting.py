from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import  ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.Enum import TranscriptStatus
from app.core.database import Base


if TYPE_CHECKING:
    from app.models.audio import Audio
    from app.models.meeting_user import MeetingUser
    from app.models.chunk import MeetingChunk
    from app.models.chat_messages import ChatMessage


    from app.models.segment import Segment


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

    '''
    NOT_STARTED
    PROCESSING
    COMPLETED
    FAILED
    '''

    transcript_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=TranscriptStatus.NOT_STARTED
    )

    embedding_status: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        default=TranscriptStatus.NOT_STARTED
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    audio_id: Mapped[int|None] = mapped_column(
    ForeignKey("audio.id"),
    unique=True,
    nullable=True
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

    chunks: Mapped[list["MeetingChunk"]] = relationship(
    back_populates="meeting",
    cascade="all, delete-orphan",
    )

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
    segments: Mapped[list["Segment"]] = relationship(
        "Segment",
        back_populates="meeting",
        cascade="all, delete-orphan",
    )