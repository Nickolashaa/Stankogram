from ..base import BaseResponse


class SystemNotificationResponse(BaseResponse):
    title: str
    text: str
