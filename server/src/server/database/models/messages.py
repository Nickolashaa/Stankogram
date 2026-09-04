from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .auth import User
from .chats import Chat


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    encrypted_text: Mapped[str]


class MessageReaction(Base):
    __tablename__ = "message_reactions"

    message_id: Mapped[int] = mapped_column(ForeignKey(Message.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    emoji: Mapped[str] = mapped_column(String(32))

    __table_args__ = (
        UniqueConstraint(
            "message_id", "user_id", "emoji", name="uq_message_user_emoji"
        ),
    )
