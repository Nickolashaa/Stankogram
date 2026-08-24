from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...enums.messages import MessageType
from ..connection import Base
from .auth import User
from .chats import Chat


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    sender_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    encrypted_text: Mapped[str]
    type: Mapped[MessageType]
