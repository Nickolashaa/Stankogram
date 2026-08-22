from typing import NotRequired, Required, Sequence, TypedDict

from ...enums.chats import ChatType


class ChatFiltersParams(TypedDict):
    type: NotRequired[ChatType]


class ChatGetListFilters(ChatFiltersParams):
    ids: NotRequired[Sequence[int]]


class ChatCreateParams(TypedDict):
    type: Required[ChatType]
    title: Required[str | None]
