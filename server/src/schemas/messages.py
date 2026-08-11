from pydantic import Field

from ..enums.messages import MessageType
from .base import BaseResponse, Schema


class MessageResponse(BaseResponse):
    chat_id: int
    type: MessageType
    text: str


class MessageCreate(Schema):
    chat_id: int
    type: MessageType
    text: str


class MessageFilters(Schema):
    chat_id: int | None = Field(None)
    type: MessageType | None = Field(None)
