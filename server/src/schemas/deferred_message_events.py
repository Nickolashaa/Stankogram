from ..enums.deferred_message_events import DeferredMessageEventType
from .base import BaseResponse


class DeferredMessageEventResponse(BaseResponse):
    message_id: int
    recipient_id: int
    type: DeferredMessageEventType
    is_delivered: bool
