from typing import NotRequired, Required, TypedDict


class MessageReactionGetListFilters(TypedDict):
    message_id: NotRequired[int]
    message_ids: NotRequired[list[int]]
    user_id: NotRequired[int]
    emoji: NotRequired[str]


class MessageReactionCreateParams(TypedDict):
    message_id: Required[int]
    user_id: Required[int]
    emoji: Required[str]
