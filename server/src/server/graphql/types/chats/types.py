from typing import Self

import strawberry

from ....services.chats.participants.schemas import ChatParticipantResponse
from ....services.chats.schemas import ChatResponse
from ...context import AppInfo, AuthorizedAppInfo
from ...permissions.chats import IsChatParticipant
from ..auth import IUser, User
from ..base import IBaseMeta, IBaseType
from ..messages import Message
from .enums import EChatType
from .interfaces import IChat


@strawberry.type
class Chat(IBaseType):
    type: EChatType
    public_title: strawberry.Private[str | None]

    @strawberry.field
    async def title(self, info: AuthorizedAppInfo) -> str:
        if self.type == EChatType.PUBLIC:
            return self.public_title or "Неизвестное название чата"

        links = await info.context.services.chat_participant_service.get_list(
            chat_id=self.id, exclude_user_ids=[info.context.current_user.id]
        )
        participant_id = [link.user_id for link in links][0]
        participant = await info.context.data_loaders.user_loader.load(participant_id)
        return participant.full_name

    @strawberry.field
    async def recipients(self, info: AppInfo) -> list[User]:
        links = await info.context.services.chat_participant_service.get_list(
            chat_id=self.id
        )
        return await info.context.data_loaders.user_loader.load_many(
            [link.user_id for link in links]
        )

    @strawberry.field(permission_classes=[IsChatParticipant])
    async def messages(self, info: AppInfo) -> list[Message]:
        return await info.context.data_loaders.messages_by_chat_id_loader.load(self.id)

    @classmethod
    def from_schema(cls, instance: ChatResponse) -> Self:
        return cls(
            id=instance.id,
            type=instance.type,
            public_title=instance.title,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class ChatParticipant(IBaseType, IUser, IChat):
    @classmethod
    def from_schema(cls, instance: ChatParticipantResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class ChatsMeta(IBaseMeta):
    chats: list[Chat]
