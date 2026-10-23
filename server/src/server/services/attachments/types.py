from typing import NotRequired, Required, Sequence, TypedDict


class AttachmentCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    name: Required[str]
    content_type: Required[str]
    size: Required[int]
    width: NotRequired[int | None]
    height: NotRequired[int | None]
    duration_ms: NotRequired[int | None]


class AttachmentGetListFilters(TypedDict):
    ids: NotRequired[Sequence[int]]
    chat_id: NotRequired[int]
    user_id: NotRequired[int]
    message_id: NotRequired[int]
    message_ids: NotRequired[Sequence[int]]
    is_attached: NotRequired[bool]
