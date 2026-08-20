from typing import NotRequired, Required, Sequence, TypedDict

from ...enums.messages import MessageType


class MessageGetListFilters(TypedDict):
    ids: NotRequired[Sequence[int]]
    chat_id: NotRequired[int]


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    type: Required[MessageType]
    text: Required[str]
