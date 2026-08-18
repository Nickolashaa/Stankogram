from ..enums.chats import ChatType
from .base import BaseResponse, Schema
from .messages import MessageResponse


class ChatResponse(BaseResponse):
    type: ChatType


class ChatProfile(Schema):
    chat: ChatResponse
    last_message: MessageResponse | None
    title: str
