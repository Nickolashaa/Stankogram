from typing import Iterable, NotRequired, Required, TypedDict

from ...enums.messages import MessageType


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    type: Required[MessageType]
    text: Required[str]


class MessageGetListFilters(TypedDict):
    ids: NotRequired[Iterable[int]]
    chat_id: NotRequired[int]
