from typing import Sequence, NotRequired, TypedDict


class MessageGetListFilters(TypedDict):
    ids: NotRequired[Sequence[int]]
    chat_id: NotRequired[int]
