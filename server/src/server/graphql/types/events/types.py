from typing import Annotated

import strawberry

from ....enums.events import EventType
from ....services.events.schemas import (
    ChatParticipantEventSchema,
    MessageEventSchema,
)
from ..chats import ChatParticipant
from ..messages import Message


@strawberry.type
class CreateMessage:
    message: Message


@strawberry.type
class UpdateMessage:
    message: Message


@strawberry.type
class DeleteMessage:
    message: Message


@strawberry.type
class AddChatParticipant:
    chat_id: int
    participant: ChatParticipant


@strawberry.type
class RemoveChatParticipant:
    chat_id: int
    participant: ChatParticipant


Event = Annotated[
    CreateMessage
    | UpdateMessage
    | DeleteMessage
    | AddChatParticipant
    | RemoveChatParticipant,
    strawberry.union("Event"),
]


def event_from_schema(
    instance: MessageEventSchema | ChatParticipantEventSchema,
) -> Event:
    if isinstance(instance, ChatParticipantEventSchema):
        participant = ChatParticipant.from_schema(instance.participant)

        if instance.type == EventType.ADD_CHAT_PARTICIPANT:
            return AddChatParticipant(
                chat_id=instance.participant.chat_id,
                participant=participant,
            )

        return RemoveChatParticipant(
            chat_id=instance.participant.chat_id,
            participant=participant,
        )

    message = Message.from_schema(instance.message)

    match instance.type:
        case EventType.CREATE_MESSAGE:
            return CreateMessage(message=message)
        case EventType.UPDATE_MESSAGE:
            return UpdateMessage(message=message)
        case EventType.DELETE_MESSAGE:
            return DeleteMessage(message=message)
