from ..base import BaseResponse


class NotificationResponse(BaseResponse):
    message_id: int
    user_id: int
    is_hidden: bool
