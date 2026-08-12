from typing import Unpack

from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from ...database.models.auth import User
from ...database.models.chats import Chat, ChatParticipant
from ...enums.chats import ChatType
from ...schemas.chats import ChatProfileResponse, ChatResponse
from ...schemas.users import UserResponse
from ..auth import AuthService
from ..base import BaseService
from ..exceptions import InvalidInput, ObjectNotFound
from .types import ChatParticipantInputParams, PrivateChatCreateParams


class ChatService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        auth_service: AuthService,
    ) -> None:
        super().__init__(session)
        self._user_service = auth_service

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
                ChatParticipantInputParams(
                    user_id=data.get("my_id"),
                    chat_id=chat.id,
                ),
                ChatParticipantInputParams(
                    user_id=data.get("participant_id"),
                    chat_id=chat.id,
                ),
            ]
        )
        await self._session.execute(add_participants_stmt)

        return ChatResponse.model_validate(chat)

    async def get_private_chat_or_create(
        self,
        **data: Unpack[PrivateChatCreateParams],
    ) -> ChatProfileResponse:
        if data.get("my_id") == data.get("participant_id"):
            raise InvalidInput("You cannot chat to yourself")

        participant = await self._user_service.get(data.get("participant_id"))

        try:
            chat = await self._get_private_chat_by_participants(**data)
        except ObjectNotFound:
            chat = await self._create_private_chat(**data)

        return ChatProfileResponse(
            chat=chat,
            title=participant.full_name,
        )

    async def is_exists(
        self,
        **data: Unpack[ChatParticipantInputParams],
    ) -> bool:
        stmt = select(exists()).where(
            ChatParticipant.user_id == data.get("user_id"),
            ChatParticipant.chat_id == data.get("chat_id"),
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_list(self, user_id: int) -> list[ChatProfileResponse]:
        other_participant = aliased(ChatParticipant)

        stmt = (
            select(Chat, User)
            .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
            .join(other_participant, other_participant.chat_id == Chat.id)
            .join(User, User.id == other_participant.user_id)
            .where(
                ChatParticipant.user_id == user_id,
                other_participant.user_id != user_id,
            )
            .order_by(Chat.created_at.desc())
        )
        res = await self._session.execute(stmt)

        return [
            ChatProfileResponse(
                chat=ChatResponse.model_validate(chat),
                title=UserResponse.model_validate(participant).full_name,
            )
            for chat, participant in res.all()
        ]
