from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ...enums.deferred_message_events import DeferredMessageEventType
from ..connection import Base
from .auth import User
from .messages import Message


class DeferredMessageEvent(Base):
    __tablename__ = "deferred_message_events"

    message_id: Mapped[int] = mapped_column(ForeignKey(Message.id, ondelete="CASCADE"))
    type: Mapped[DeferredMessageEventType]
    recipient_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    is_delivered: Mapped[bool] = mapped_column(server_default=expression.false())
