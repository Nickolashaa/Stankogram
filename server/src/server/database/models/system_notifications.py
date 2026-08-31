from sqlalchemy import ForeignKey, UniqueConstraint
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
        ForeignKey(
            SystemNotification.id,
            ondelete="CASCADE",
            name="fk_read_system_notifications_system_notification_id",
        )
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "system_notification_id",
            name="uq_user_system_notification",
        ),
    )
