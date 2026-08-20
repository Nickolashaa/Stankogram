from typing import NotRequired, Required, TypedDict


class ChatParticipantCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]


class ChatParticipantGetListFilters(TypedDict):
    chat_id: NotRequired[int]
