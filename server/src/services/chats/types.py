from typing import Required, TypedDict

from ...enums.chats import ChatType


class ChatCreateParams(TypedDict):
    type: Required[ChatType]
