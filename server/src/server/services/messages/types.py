from typing import NotRequired, Required, TypedDict


class MessageGetListFilters(TypedDict):
    chat_id: NotRequired[int]
    chat_ids: NotRequired[list[int]]


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    text: Required[str]
