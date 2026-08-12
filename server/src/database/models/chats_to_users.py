from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .chats import Chat
from .users import User


class ChatToUser(Base):
    __tablename__ = "chats_to_users"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("user_id", "chat_id", name="uq_user_chat"),)
