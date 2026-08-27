from datetime import datetime
from typing import NotRequired, Required, Sequence, TypedDict


class ChatParticipantCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    is_admin: NotRequired[bool]
    is_muted: NotRequired[bool]
    last_read_at: NotRequired[datetime]


class ChatParticipantGetListFilters(TypedDict):
    chat_id: NotRequired[int]
    user_ids: NotRequired[Sequence[int]]
    exclude_user_ids: NotRequired[Sequence[int]]
    user_id: NotRequired[int]
    is_admin: NotRequired[bool]
    is_muted: NotRequired[bool]
