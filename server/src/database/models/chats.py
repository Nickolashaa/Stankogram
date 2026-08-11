from enum import StrEnum

from sqlalchemy.orm import Mapped

from ..connection import Base


class ChatType(StrEnum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class Chat(Base):
    __tablename__ = "chats"

    type: Mapped[ChatType]
