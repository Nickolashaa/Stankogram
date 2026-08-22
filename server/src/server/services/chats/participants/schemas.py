from ...base import BaseResponse


class ChatParticipantResponse(BaseResponse):
    chat_id: int
    user_id: int
