from ..enums.chats import ChatType
from .base import BaseResponse


class ChatResponse(BaseResponse):
    type: ChatType
