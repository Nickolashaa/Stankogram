from typing import Self

import strawberry

from ....services.messages.reactions.schemas import MessageReactionResponse
from ....services.messages.schemas import MessageResponse
from ...context import AppInfo
from ..auth import IUser
from ..base import IBaseMeta, IBaseType
from ..chats import IChat


@strawberry.type
class MessageReaction(IBaseType, IUser):
    message_id: strawberry.Private[int]
    emoji: str

    @classmethod
    def from_schema(cls, instance: MessageReactionResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            message_id=instance.message_id,
            emoji=instance.emoji,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class Message(IBaseType, IUser, IChat):
    text: str

    @strawberry.field
    async def reactions(self, info: AppInfo) -> list[MessageReaction]:
        return await info.context.data_loaders.reactions_by_message_id_loader.load(
            key=self.id
        )

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
class MessageReactionsUpdated:
    message: Message


@strawberry.type
class MessagesMeta(IBaseMeta):
    messages: list[Message]
