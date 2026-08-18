from typing import Unpack

from sqlalchemy import insert, select

from ....database.models.chats import Chat, ChatParticipant
from ....enums.chats import ChatType
from ....exceptions import InvalidInput, ObjectNotFound
from ...base import BaseService
from .types import (
    PrivateChatCreateParams,
)
from ....schemas.chats import ChatResponse


class PrivateChatService(BaseService):
    async def _get_private_chat_by_participants(
        self,
        **data: Unpack[PrivateChatCreateParams],
    ) -> ChatResponse:
        stmt = (
            select(Chat)
            .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
            .where(
                Chat.type == ChatType.PRIVATE,
                ChatParticipant.user_id.in_(data.values()),
            )
            .limit(1)
        )

        res = await self._session.execute(stmt)
        chat = res.scalar_one_or_none()
        if chat is None:
            raise ObjectNotFound(
                f"Private chat with participant {data.get('participant_id')} not found"
            )

        return ChatResponse.model_validate(chat)

    async def _create_private_chat(
        self,
        **data: Unpack[PrivateChatCreateParams],
    ) -> ChatResponse:
        create_chat_stmt = insert(Chat).values(type=ChatType.PRIVATE).returning(Chat)
        create_chat_res = await self._session.execute(create_chat_stmt)
        chat = create_chat_res.scalar_one()

        add_participants_stmt = insert(ChatParticipant).values(
            [
                {
                    "user_id": data.get("user_id"),
                    "chat_id": chat.id,
                },
                {
                    "user_id": data.get("participant_id"),
                    "chat_id": chat.id,
                },
            ]
        )
        await self._session.execute(add_participants_stmt)

        return ChatResponse.model_validate(chat)

    async def get_private_chat_or_create(
        self,
        **data: Unpack[PrivateChatCreateParams],
    ) -> ChatResponse:
        if data.get("user_id") == data.get("participant_id"):
            raise InvalidInput("You cannot chat to yourself")

        try:
            return await self._get_private_chat_by_participants(**data)
        except ObjectNotFound:
            return await self._create_private_chat(**data)
