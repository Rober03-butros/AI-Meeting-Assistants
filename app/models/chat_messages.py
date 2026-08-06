from datetime import datetime

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.meeting import Meeting
    from app.models.user import User

class ChatMessage(Base):

    __tablename__ = "chat_messages"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id")
    )


    question: Mapped[str]

    rewritten_question: Mapped[str | None]

    answer: Mapped[str] = mapped_column(
        nullable=True,
    )

    sources: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )


    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="chat_messages",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="chat_messages",
    )