from typing import Self

import strawberry

from ....enums.events import EventType
from ....services.events.schemas import MessageEventSchema
from ....services.messages.schemas import MessageResponse
from ...context import AppInfo
from ..auth import IUser
from ..base import IBaseMeta, IBaseType
from ..chats import IChat


@strawberry.type
class Message(IBaseType, IUser, IChat):
    text: str
    reply_to_message_id: strawberry.Private[int | None]

    @strawberry.field
    async def reply_to(self, info: AppInfo) -> "Message | None":
        if self.reply_to_message_id is None:
            return None

        return await info.context.data_loaders.message_loader.load(
            self.reply_to_message_id
        )

    @classmethod
    def from_schema(cls, instance: MessageResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            text=instance.text,
            reply_to_message_id=instance.reply_to_message_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class MessagesMeta(IBaseMeta):
    messages: list[Message]


@strawberry.type
class CreateMessage:
    message: Message


@strawberry.type
class UpdateMessage:
    message: Message


@strawberry.type
class DeleteMessage:
    message: Message


Event = CreateMessage | UpdateMessage | DeleteMessage


def event_from_schema(instance: MessageEventSchema) -> Event:
    message = Message.from_schema(instance.message)

    match instance.type:
        case EventType.CREATE_MESSAGE:
            return CreateMessage(message=message)
        case EventType.UPDATE_MESSAGE:
            return UpdateMessage(message=message)
        case EventType.DELETE_MESSAGE:
            return DeleteMessage(message=message)
