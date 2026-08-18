from typing import NotRequired, Required, Sequence, TypedDict


class PublicChatCreateParams(TypedDict):
    title: Required[str]
    participant_ids: NotRequired[Sequence[int]]
