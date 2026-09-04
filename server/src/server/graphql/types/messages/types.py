from typing import Self

import strawberry

from ....services.messages.schemas import MessageResponse
from ..auth import IUser
from ..base import IBaseMeta, IBaseType
from ..chats import IChat


@strawberry.type
class Message(IBaseType, IUser, IChat):
    text: str

    @classmethod
    def from_schema(cls, instance: MessageResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            text=instance.text,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class MessagesMeta(IBaseMeta):
    messages: list[Message]
