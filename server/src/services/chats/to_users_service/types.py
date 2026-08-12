from typing import NotRequired, Required, TypedDict


class ChatToUserParams(TypedDict):
    user_id: Required[int]
    chat_id: Required[int]


class ChatToUserGetListFilters(TypedDict):
    user_id: NotRequired[int]
    chat_id: NotRequired[int]
