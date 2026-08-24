from typing import Self

import strawberry

from ....services.messages.schemas import MessageResponse
from ..auth import IUser
from ..base import IBaseType
from ..chats import IChat
from .enums import EMessageType


@strawberry.type
class Message(IBaseType, IUser, IChat):
    text: str
    type: EMessageType

    @classmethod
    def from_schema(cls, instance: MessageResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            text=instance.text,
            type=instance.type,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
