from ..enums.chats import ChatType
from .base import BaseResponse, Schema
from .messages import MessageResponse


class ChatResponse(BaseResponse):
    type: ChatType


class PublicChatProfileResponse(BaseResponse):
    title: str
    chat_id: int


class ChatProfile(Schema):
    chat: ChatResponse
    last_message: MessageResponse | None
    title: str


class ChatParticipantResponse(BaseResponse):
    chat_id: int
    user_id: int
