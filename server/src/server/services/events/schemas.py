from ...enums.events import EventType
from ..base import Schema
from ..messages.schemas import MessageResponse


class MessageEventSchema(Schema):
    type: EventType
    message: MessageResponse
