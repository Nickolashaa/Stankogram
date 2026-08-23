from typing import NotRequired, Required, Sequence, TypedDict


class ChatParticipantCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    is_admin: Required[bool]
    is_muted: Required[bool]


class ChatParticipantGetListFilters(TypedDict):
    chat_id: NotRequired[int]
    exclude_user_ids: NotRequired[Sequence[int]]
    user_id: NotRequired[int]
    is_admin: NotRequired[bool]
    is_muted: NotRequired[bool]
