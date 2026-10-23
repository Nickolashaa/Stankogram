from ...enums.attachments import AttachmentKind
from ..base import BaseResponse


class AttachmentResponse(BaseResponse):
    chat_id: int
    user_id: int
    message_id: int | None
    kind: AttachmentKind
    key: str
    thumbnail_key: str | None
    name: str
    content_type: str
    size: int
    width: int | None
    height: int | None
    duration_ms: int | None
