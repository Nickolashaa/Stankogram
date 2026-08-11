from ..enums.chats import ChatType
from .base import BaseResponse, Schema


class ChatInput(Schema):
    type: ChatType


class ChatResponse(BaseResponse):
    type: ChatType
