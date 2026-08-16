from typing import Self

from cryptography.fernet import Fernet
from pydantic import Field

from ..database.models.messages import Message
from ..enums.messages import MessageType
from .base import BaseResponse, PaginationSchema, Schema


class MessageResponse(BaseResponse):
    chat_id: int
    user_id: int
    type: MessageType
    text: str

    @classmethod
    def from_ORM(cls, fernet: Fernet, instance: Message) -> Self:
        return cls(
            id=instance.id,
            chat_id=instance.chat_id,
            user_id=instance.user_id,
            type=instance.type,
            text=fernet.decrypt(instance.encrypted_text.encode()).decode(),
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


class MessageCreate(Schema):
    chat_id: int
    type: MessageType
    text: str


class MessageFilters(Schema):
    chat_id: int | None = Field(None)


class MessageListQuery(MessageFilters, PaginationSchema):
    pass
