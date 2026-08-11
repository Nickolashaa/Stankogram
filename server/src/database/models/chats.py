from sqlalchemy.orm import Mapped

from ...enums.chats import ChatType
from ..connection import Base


class Chat(Base):
    __tablename__ = "chats"

    type: Mapped[ChatType]
