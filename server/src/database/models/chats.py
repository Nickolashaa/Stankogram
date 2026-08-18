from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ...enums.chats import ChatType
from ..connection import Base
from .auth import User


class Chat(Base):
    __tablename__ = "chats"

    type: Mapped[ChatType]


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_user_chat"),)


class PublicChatProfile(Base):
    __tablename__ = "public_chat_profiles"

    title: Mapped[str]
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    last_message_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE")
    )
