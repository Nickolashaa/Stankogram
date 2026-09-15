from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ..connection import Base
from .auth import User
from .messages import Message


class Notification(Base):
    __tablename__ = "notifications"

    message_id: Mapped[int] = mapped_column(
        ForeignKey(Message.id, ondelete="CASCADE"),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"),
    )
    is_hidden: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )

    __table_args__ = (
        UniqueConstraint(
            "message_id",
            "user_id",
            name="uq_notification_message_user",
        ),
    )
