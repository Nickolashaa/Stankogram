from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ...enums.chats import ChatType
from ..connection import Base
from .auth import User


class Chat(Base):
    __tablename__ = "chats"

    type: Mapped[ChatType]
    title: Mapped[str | None]


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    is_admin: Mapped[bool] = mapped_column(server_default=expression.false())
    is_muted: Mapped[bool] = mapped_column(server_default=expression.false())

    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_user_chat"),)
