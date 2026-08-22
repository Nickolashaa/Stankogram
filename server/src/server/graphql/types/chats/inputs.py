import strawberry

from ....services.chats.participants.types import ChatParticipantGetListFilters
from ....services.chats.types import ChatFiltersParams
from .enums import EChatType


@strawberry.input
class ChatFiltersIn:
    type: strawberry.Maybe[EChatType]

    def to_service_params(self) -> ChatFiltersParams:
        params: ChatFiltersParams = {}

        if self.type is not None:
            params["type"] = self.type.value

        return params


@strawberry.input
class ChatParticipantFiltersIn:
    user_id: strawberry.Maybe[int]
    chat_id: strawberry.Maybe[int]

    def to_service_params(self) -> ChatParticipantGetListFilters:
        params: ChatParticipantGetListFilters = {}

        if self.user_id is not None:
            params["user_id"] = self.user_id.value

        if self.chat_id is not None:
            params["chat_id"] = self.chat_id.value

        return params
