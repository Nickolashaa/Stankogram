import strawberry

from ....enums.chats import ChatType
from ....services.chats.participants.types import (
    ChatParticipantCreateParams,
    ChatParticipantGetListFilters,
)
from ....services.chats.types import (
    ChatCreateParams,
    ChatFiltersParams,
    ChatUpdateParams,
)
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


@strawberry.input
class PublicChatIn:
    title: str
    participant_ids: list[int] | None

    def to_service_params(self) -> ChatCreateParams:
        return ChatCreateParams(
            type=ChatType.PUBLIC,
            title=self.title,
        )


@strawberry.input
class PrivateChatIn:
    participant_id: int

    def to_service_params(self) -> ChatCreateParams:
        return ChatCreateParams(
            type=ChatType.PRIVATE,
            title=None,
        )


@strawberry.input
class ChatUpdateIn:
    title: str

    def to_service_params(self) -> ChatUpdateParams:
        return ChatUpdateParams(title=self.title)


@strawberry.input
class ChatParticipantIn:
    chat_id: int
    user_id: int
    is_admin: bool
    is_muted: bool

    def to_create_service_params(self) -> ChatParticipantCreateParams:
        return ChatParticipantCreateParams(
            chat_id=self.chat_id,
            user_id=self.user_id,
            is_admin=self.is_admin,
            is_muted=self.is_muted,
        )
