import strawberry

from ....services.messages.types import MessageGetListFilters


@strawberry.input
class MessageFiltersIn:
    chat_id: int

    def to_service_params(self) -> MessageGetListFilters:
        return MessageGetListFilters(chat_id=self.chat_id)


@strawberry.input
class MessageIn:
    chat_id: int
    text: str
