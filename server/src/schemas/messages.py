from pydantic import Field

from ..enums.messages import MessageType
from .base import BaseResponse, PaginationSchema, Schema


class MessageResponse(BaseResponse):
    chat_id: int
    user_id: int
    type: MessageType
    text: str


class MessageCreate(Schema):
    chat_id: int
    type: MessageType
    text: str


class MessageFilters(Schema):
    chat_id: int | None = Field(None)
    user_id: int | None = Field(None)


class MessageListQuery(MessageFilters, PaginationSchema):
    pass
