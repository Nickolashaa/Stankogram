from typing import NotRequired, Required, TypedDict

from ...enums.deferred_message_events import DeferredMessageEventType


class DeferredMessageEventCreateParams(TypedDict):
    message_id: Required[int]
    recipient_id: Required[int]
    type: Required[DeferredMessageEventType]


class DeferredMessageEventGetListFilters(TypedDict):
    recipient_id: NotRequired[int]
    is_delivered: NotRequired[bool]
