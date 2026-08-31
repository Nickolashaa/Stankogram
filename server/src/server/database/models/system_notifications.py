from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .auth import User


class SystemNotification(Base):
    __tablename__ = "system_notifications"

    text: Mapped[str]


class ReadSystemNotification(Base):
    __tablename__ = "read_system_notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    system_notification_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE")
    )
