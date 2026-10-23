from typing import Annotated, Literal

from pydantic import Field

from ...enums.events import EventType
from ..base import Schema
from ..chats.participants.schemas import ChatParticipantResponse
from ..messages.schemas import MessageResponse


class MessageEventSchema(Schema):
    type: Literal[
        EventType.CREATE_MESSAGE,
        EventType.UPDATE_MESSAGE,
        EventType.DELETE_MESSAGE,
    ]
    message: MessageResponse


class ChatParticipantEventSchema(Schema):
    type: Literal[
        EventType.ADD_CHAT_PARTICIPANT,
        EventType.REMOVE_CHAT_PARTICIPANT,
    ]
    participant: ChatParticipantResponse


EventSchema = Annotated[
    MessageEventSchema | ChatParticipantEventSchema,
    Field(discriminator="type"),
]
