import strawberry

from ....services.messages.types import MessageGetListFilters
from .enums import EMessageType


@strawberry.input
class MessageFiltersIn:
    chat_id: int
    type: strawberry.Maybe[EMessageType]

    def to_service_params(self) -> MessageGetListFilters:
        params: MessageGetListFilters = {"chat_id": self.chat_id}

        if self.type is not None:
            params["type"] = self.type.value

        return params
