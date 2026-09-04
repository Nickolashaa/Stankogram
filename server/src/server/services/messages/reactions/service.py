from typing import Unpack

from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError

from ....database.models.messages import MessageReaction
from ...base import BasePagination, BaseService
from ...exceptions import InvalidInput, ObjectNotFound
from .schemas import MessageReactionResponse
from .types import MessageReactionCreateParams, MessageReactionGetListFilters

MAX_EMOJI_LENGTH = 32


class MessageReactionService(BaseService):
    async def create(
        self,
        **values: Unpack[MessageReactionCreateParams],
    ) -> MessageReactionResponse:
        stmt = insert(MessageReaction).values(**values).returning(MessageReaction)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            if "fk_message_reactions_message_id" in str(e.orig):
                raise ObjectNotFound(
                    f"Message with id {values.get('message_id')} not found"
                )
            raise

        return MessageReactionResponse.model_validate(res.scalar_one())

    async def delete(self, id: int) -> None:
        stmt = delete(MessageReaction).where(MessageReaction.id == id)
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[MessageReaction]],
        **filters: Unpack[MessageReactionGetListFilters],
    ) -> Select[tuple[MessageReaction]]:
        if (message_id := filters.get("message_id")) is not None:
            stmt = stmt.where(MessageReaction.message_id == message_id)

        if (message_ids := filters.get("message_ids")) is not None:
            stmt = stmt.where(MessageReaction.message_id.in_(message_ids))

        if (user_id := filters.get("user_id")) is not None:
            stmt = stmt.where(MessageReaction.user_id == user_id)

        if (emoji := filters.get("emoji")) is not None:
            stmt = stmt.where(MessageReaction.emoji == emoji)

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[MessageReactionGetListFilters],
    ) -> list[MessageReactionResponse]:
        stmt = select(MessageReaction).order_by(MessageReaction.id)

        stmt = self._apply_filters(stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            MessageReactionResponse.model_validate(entity)
            for entity in res.scalars().all()
        ]

    async def get_or_none(
        self,
        message_id: int,
        user_id: int,
        emoji: str,
    ) -> MessageReactionResponse | None:
        stmt = select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == user_id,
            MessageReaction.emoji == emoji,
        )
        res = await self._session.execute(stmt)
        instance = res.scalar_one_or_none()
        if instance is None:
            return None
        return MessageReactionResponse.model_validate(instance)

    async def toggle(
        self,
        **values: Unpack[MessageReactionCreateParams],
    ) -> bool:
        emoji = values["emoji"]
        if not emoji.strip() or len(emoji) > MAX_EMOJI_LENGTH:
            raise InvalidInput("Reaction must be a single emoji")

        existing = await self.get_or_none(
            message_id=values["message_id"],
            user_id=values["user_id"],
            emoji=values["emoji"],
        )

        if existing is not None:
            await self.delete(existing.id)
            return False

        await self.create(**values)
        return True
