from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base


if TYPE_CHECKING:
    from app.models.meeting import Meeting
    from app.models.user import User


class MeetingUser(Base):

    __tablename__ = "meeting_users"


    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"),
        primary_key=True,
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        primary_key=True,
    )


    role: Mapped[str] = mapped_column(
        String(20),
        default="member",
        nullable=False,
    )


    meeting: Mapped["Meeting"] = relationship(
        "Meeting",
        back_populates="users",
    )


    user: Mapped["User"] = relationship(
        "User",
        back_populates="meetings",
    )

    __table_args__ = (
    UniqueConstraint(
        "meeting_id",
        "user_id",
        name="unique_meeting_user"
    ),
    )