from typing import Required, TypedDict, NotRequired, Sequence


class PrivateChatCreateParams(TypedDict):
    user_id: Required[int]
    participant_id: Required[int]
