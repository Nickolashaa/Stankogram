from typing import Required, TypedDict


class ChatRecipientsCreateParams(TypedDict):
    user_id: Required[int]
    chat_id: Required[int]
