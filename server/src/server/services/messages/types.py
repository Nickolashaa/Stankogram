from typing import NotRequired, Required, TypedDict

from ...enums.messages import MessageType


class MessageGetListFilters(TypedDict):
    chat_id: NotRequired[int]
    chat_ids: NotRequired[list[int]]
    type: NotRequired[MessageType]


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    type: Required[MessageType]
    text: Required[str]
