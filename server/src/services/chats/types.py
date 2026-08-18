from typing import Required, TypedDict

from ...enums.messages import MessageType


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    type: Required[MessageType]
    text: Required[str]
