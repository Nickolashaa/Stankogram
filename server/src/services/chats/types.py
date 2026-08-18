from ...enums.messages import MessageType
from typing import TypedDict, Required


class MessageCreateParams(TypedDict):
    chat_id: Required[int]
    user_id: Required[int]
    type: Required[MessageType]
    text: Required[str]