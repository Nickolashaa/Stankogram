from typing import Self

import strawberry

from ....services.chats.schemas import ChatResponse
from ...context import AppInfo
from ..auth import IUser, User
from ..base import IBaseType
from ..errors import UnauthorizedError
from .enums import EChatType
from .interfaces import IChat


@strawberry.type
class Chat(IBaseType):
    type: EChatType
    public_title: strawberry.Private[str | None]

    @strawberry.field
    async def title(self, info: AppInfo) -> str | UnauthorizedError:
        if self.type == EChatType.PUBLIC:
            return self.public_title or "Неизвестное название чата"

        if info.context.current_user is None:
            return UnauthorizedError(message="User not authorized")

        links = await info.context.services.chat_participant_service.get_list(
            chat_id=self.id
        )
        participant_id = [
            link.user_id
            for link in links
            if link.user_id != info.context.current_user.id
        ][0]
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
    pass
