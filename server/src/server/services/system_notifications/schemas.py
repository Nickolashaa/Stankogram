from datetime import datetime

from ..base import BaseResponse


class SystemNotificationResponse(BaseResponse):
    title: str
    text: str
    expires_at: datetime | None
