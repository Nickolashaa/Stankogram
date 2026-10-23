from typing import Self

from cryptography.fernet import Fernet

from ...database.models.messages import Message
from ..base import BaseResponse


class MessageResponse(BaseResponse):
    chat_id: int
    user_id: int
    text: str
    reply_to_message_id: int | None

    @classmethod
    def from_ORM(cls, instance: Message, fernet: Fernet) -> Self:
        return cls(
            id=instance.id,
            chat_id=instance.chat_id,
            user_id=instance.user_id,
            text=fernet.decrypt(instance.encrypted_text.encode()).decode(),
            reply_to_message_id=instance.reply_to_message_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
