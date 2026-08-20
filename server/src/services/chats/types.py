from typing import NotRequired, Required, Sequence, TypedDict

from ...enums.chats import ChatType


class ChatGetListFilters(TypedDict):
    type: NotRequired[ChatType]
    ids: NotRequired[Sequence[int]]


class ChatCreateParams(TypedDict):
    type: Required[ChatType]
    title: Required[str | None]
