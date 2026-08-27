from datetime import datetime

from ...base import BaseResponse


class ChatParticipantResponse(BaseResponse):
    chat_id: int
    user_id: int
    is_admin: bool
    is_muted: bool
    last_read_at: datetime | None
