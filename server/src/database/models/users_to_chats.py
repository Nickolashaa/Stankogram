from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base
from .chats import Chat
from .users import User


class UsersToChats(Base):
    __tablename__ = "users_to_chats"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
