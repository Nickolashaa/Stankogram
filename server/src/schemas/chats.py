from ..enums.chats import ChatType
from .base import BaseResponse, Schema


class ChatInput(Schema):
    type: ChatType


class ChatResponse(BaseResponse):
    type: ChatType


class PrivateChatParticipants(Schema):
    first_user_id: int
    second_user_id: int
