from typing import NotRequired, Sequence, TypedDict


class MessageGetListFilters(TypedDict):
    ids: NotRequired[Sequence[int]]
    chat_id: NotRequired[int]
