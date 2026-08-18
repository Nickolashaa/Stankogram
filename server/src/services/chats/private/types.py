from typing import Required, TypedDict


class PrivateChatCreateParams(TypedDict):
    user_id: Required[int]
    participant_id: Required[int]
