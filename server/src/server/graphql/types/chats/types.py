from datetime import datetime
from typing import Self

import strawberry

from ....services.chats.participants.schemas import ChatParticipantResponse
from ....services.chats.schemas import ChatResponse
from ...context import AppInfo, AuthorizedAppInfo
from ...permissions.chats import IsChatParticipant
from ..auth import IUser
from ..base import IBaseMeta, IBaseType
from ..messages import Message
from .enums import EChatType
from .interfaces import IChat


@strawberry.type
class ChatParticipant(IBaseType, IUser, IChat):
    is_admin: bool
    is_muted: bool
    last_read_at: datetime | None

    @classmethod
    def from_schema(cls, instance: ChatParticipantResponse) -> Self:
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            is_admin=instance.is_admin,
            is_muted=instance.is_muted,
            last_read_at=instance.last_read_at,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


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
    async def participants(self, info: AppInfo) -> list[ChatParticipant]:
        links = await info.context.services.chat_participant_service.get_list(
            chat_id=self.id
        )
        return [ChatParticipant.from_schema(link) for link in links]

    @strawberry.field(permission_classes=[IsChatParticipant])
    async def last_message(self, info: AppInfo) -> Message | None:
        return await info.context.data_loaders.last_message_by_chat_id_loader.load(
            self.id
        )

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
class ChatsMeta(IBaseMeta):
    chats: list[Chat]
