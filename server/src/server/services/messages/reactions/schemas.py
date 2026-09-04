from ...base import BaseResponse


class MessageReactionResponse(BaseResponse):
    message_id: int
    user_id: int
    emoji: str
