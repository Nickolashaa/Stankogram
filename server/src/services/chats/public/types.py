from typing import Required, TypedDict, NotRequired, Sequence



class PublicChatCreateParams(TypedDict):
    title: Required[str]
    participant_ids: NotRequired[Sequence[int]]
