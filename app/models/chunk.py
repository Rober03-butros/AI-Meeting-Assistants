from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.meeting import Meeting


class MeetingChunk(Base):

    __tablename__ = "meeting_chunks"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"),
        nullable=False,
    )


    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )


    content: Mapped[str] = mapped_column(
        nullable=False,
    )


    start_time: Mapped[float] = mapped_column(
        nullable=False,
    )


    end_time: Mapped[float] = mapped_column(
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
    )


    meeting: Mapped["Meeting"] = relationship(
        back_populates="chunks",
    )