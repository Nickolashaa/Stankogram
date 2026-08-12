from typing import Required, TypedDict


class ChatParticipantInputParams(TypedDict):
    user_id: Required[int]
    chat_id: Required[int]


class PrivateChatCreateParams(TypedDict):
    my_id: Required[int]
    participant_id: Required[int]
