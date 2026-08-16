from typing import Unpack

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from ...database.models.deferred_message_events import DeferredMessageEvent
from ...exceptions import ObjectNotFound
from ...schemas.deferred_message_events import DeferredMessageEventResponse
from ..base import BaseService
from .types import DeferredMessageEventCreateParams, DeferredMessageEventGetListFilters


class DeferredMessageEventService(BaseService):
    async def create(
        self,
        **data: Unpack[DeferredMessageEventCreateParams],
    ) -> DeferredMessageEventResponse:
        stmt = (
            insert(DeferredMessageEvent).values(**data).returning(DeferredMessageEvent)
        )

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            if "fk_deferred_message_events_message_id" in str(e.orig):
                raise ObjectNotFound(
                    f"Message with id {data.get('message_id')} not found"
                )
            if "fk_deferred_message_events_recipient_id" in str(e.orig):
                raise ObjectNotFound(
                    f"User with id {data.get('recipient_id')} not found"
                )
            raise

        return DeferredMessageEventResponse.model_validate(res.scalar_one())

    async def mark_as_delivered(
        self,
        id: int,
    ) -> DeferredMessageEventResponse:
        stmt = (
            update(DeferredMessageEvent)
            .where(DeferredMessageEvent.id == id)
            .values(is_delivered=True)
            .returning(DeferredMessageEvent)
        )

        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFound(f"DeferredMessageEvent with id {id} not found")
        return DeferredMessageEventResponse.model_validate(res.scalar_one())

    async def get_list(
        self,
        **filters: Unpack[DeferredMessageEventGetListFilters],
    ) -> list[DeferredMessageEventResponse]:
        stmt = select(DeferredMessageEvent).order_by(DeferredMessageEvent.created_at)

        if (recipient_id := filters.get("recipient_id")) is not None:
            stmt = stmt.where(DeferredMessageEvent.recipient_id == recipient_id)

        if (is_delivered := filters.get("is_delivered")) is not None:
            stmt = stmt.where(DeferredMessageEvent.is_delivered == is_delivered)

        res = await self._session.execute(stmt)

        return [
            DeferredMessageEventResponse.model_validate(entity)
            for entity in res.scalars().all()
        ]
