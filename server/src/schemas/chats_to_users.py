from pydantic import Field

from .base import BaseResponse, Schema


class ChatToUserInput(Schema):
    user_id: int
    chat_id: int


class ChatToUserInputResponse(BaseResponse):
    user_id: int
    chat_id: int


class ChatToUserInputFilters(Schema):
    user_id: int | None = Field(None)
    chat_id: int | None = Field(None)
