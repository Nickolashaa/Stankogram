import strawberry

from ....services.messages.types import MessageGetListFilters, MessageUpdateParams


@strawberry.input
class MessageFiltersIn:
    chat_id: int

    def to_service_params(self) -> MessageGetListFilters:
        return MessageGetListFilters(chat_id=self.chat_id)


@strawberry.input
class MessageIn:
    chat_id: int
    text: str
    mentioned_user_ids: list[int]


@strawberry.input
class MessageUpdateIn:
    text: str
    mentioned_user_ids: list[int]

    def to_service_params(self) -> MessageUpdateParams:
        return MessageUpdateParams(text=self.text)
