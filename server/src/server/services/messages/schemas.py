from typing import Self

from cryptography.fernet import Fernet

from ...database.models.messages import Message
from ...enums.messages import MessageType
from ..base import BaseResponse


class MessageResponse(BaseResponse):
    chat_id: int
    user_id: int
    type: MessageType
    text: str

    @classmethod
    def from_ORM(cls, instance: Message, fernet: Fernet) -> Self:
        return cls(
            id=instance.id,
            chat_id=instance.chat_id,
            user_id=instance.user_id,
            type=instance.type,
            text=fernet.decrypt(instance.encrypted_text.encode()).decode(),
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
