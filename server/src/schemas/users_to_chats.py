from pydantic import Field

from .base import BaseResponse, Schema


class UsersToChatsInput(Schema):
    user_id: int
    chat_id: int


class UsersToChatsResponse(BaseResponse):
    user_id: int
    chat_id: int


class UsersToChatsFilters(Schema):
    user_id: int | None = Field(None)
    chat_id: int | None = Field(None)
