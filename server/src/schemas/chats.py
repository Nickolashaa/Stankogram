from pydantic import Field

from ..enums.chats import ChatType
from .base import BaseResponse, Schema


class ChatResponse(BaseResponse):
    type: ChatType


class PrivateChatParticipants(Schema):
    participant_ids: list[int] = Field(..., min_length=2, max_length=2)
