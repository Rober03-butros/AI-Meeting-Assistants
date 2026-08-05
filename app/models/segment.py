from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.meeting import Meeting
from app.core.database import Base

class Segment(Base):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"),
        nullable=False
    )

    start_time: Mapped[float] = mapped_column(
        nullable=False
    )

    end_time: Mapped[float] = mapped_column(
        nullable=False
    )
    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    segment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    decisions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="segments"
    )