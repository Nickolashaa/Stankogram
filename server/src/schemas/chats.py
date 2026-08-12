from ..enums.chats import ChatType
from .base import BaseResponse, Schema


class ChatResponse(BaseResponse):
    type: ChatType


class ChatProfileResponse(Schema):
    chat: ChatResponse
    title: str
