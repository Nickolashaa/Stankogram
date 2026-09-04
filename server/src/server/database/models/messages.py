from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .auth import User
from .chats import Chat


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    encrypted_text: Mapped[str]
