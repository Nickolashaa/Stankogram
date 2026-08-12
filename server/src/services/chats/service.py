from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from ...database.models.chats import Chat, ChatParticipant
from ...enums.chats import ChatType
from ...schemas.chats import ChatResponse
from ..base import BaseService
from ..exceptions import InvalidInputData, ObjectNotFound
from .types import ChatRecipientsCreateParams


class ChatService(BaseService):
    async def _get_private_chat_by_participants(
        self, participant_ids: list[int]
    ) -> ChatResponse:
        stmt = (
            select(Chat)
            .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
            .where(
                Chat.type == ChatType.PRIVATE,
                ChatParticipant.user_id.in_(participant_ids),
            )
            .limit(1)
        )

        res = await self._session.execute(stmt)
        chat = res.scalar_one_or_none()
        if chat is None:
            raise ObjectNotFound(
                f"Private chat with participants {participant_ids} not found"
            )

        return ChatResponse.model_validate(chat)

    async def get_private_chat_or_create(
        self,
        participant_ids: list[int],
    ) -> ChatResponse:
        try:
            return await self._get_private_chat_by_participants(participant_ids)
        except ObjectNotFound:
            return await self._create_private_chat(participant_ids)

    async def _create_private_chat(
        self,
        participant_ids: list[int],
    ) -> ChatResponse:
        if len(participant_ids) != 2:
            raise InvalidInputData("Private chat can have only 2 participants")

        create_chat_stmt = insert(Chat).values(type=ChatType.PRIVATE).returning(Chat)
        create_chat_res = await self._session.execute(create_chat_stmt)
        chat = create_chat_res.scalar_one()

        add_participants_stmt = insert(ChatParticipant).values(
            [
                ChatRecipientsCreateParams(
                    user_id=participant_id,
                    chat_id=chat.id,
                )
                for participant_id in participant_ids
            ]
        )
        try:
            await self._session.execute(add_participants_stmt)
        except IntegrityError:
            raise ObjectNotFound(f"Users with ids {participant_ids} not found")

        return ChatResponse.model_validate(chat)


