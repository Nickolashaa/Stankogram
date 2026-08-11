from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .chats import Chat


class MessageType(StrEnum):
    TEXT = "TEXT"


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    encrypted_text: Mapped[str]
    type: Mapped[MessageType]
