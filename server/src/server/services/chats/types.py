from typing import NotRequired, Required, Sequence, TypedDict

from ...enums.chats import ChatType


class ChatFiltersParams(TypedDict):
    type: NotRequired[ChatType]
    search_query: NotRequired[str]


class ChatGetListFilters(ChatFiltersParams):
    ids: NotRequired[Sequence[int]]
    search_exclude_user_id: NotRequired[int]


class ChatCreateParams(TypedDict):
    type: Required[ChatType]
    title: Required[str | None]


class ChatUpdateParams(TypedDict):
    title: Required[str]
