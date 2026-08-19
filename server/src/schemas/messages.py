from typing import Self

from cryptography.fernet import Fernet

from ..database.models.messages import Message
from ..enums.messages import MessageType
from .base import BaseResponse, PaginationSchema, Schema
from .users import UserResponse


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
    chat_id: int


class MessageListQuery(MessageFilters, PaginationSchema):
    pass


class MessageProfile(Schema):
    message: MessageResponse
    author: UserResponse
