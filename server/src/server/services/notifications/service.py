from typing import Sequence, Unpack

from sqlalchemy import Select, delete, insert, select, update

from ...database.models.notifications import Notification
from ..base import BasePagination, BaseService
from ..exceptions import ObjectNotFound
from .schemas import NotificationResponse
from .types import NotificationGetListFilters


class NotificationService(BaseService):
    async def sync_for_message(
        self,
        message_id: int,
        user_ids: Sequence[int],
    ) -> None:
        unique_user_ids = list(dict.fromkeys(user_ids))

        stmt = delete(Notification).where(
            Notification.message_id == message_id,
            Notification.user_id.notin_(unique_user_ids),
        )
        await self._execute(stmt)

        if not unique_user_ids:
            return

        stmt = select(Notification.user_id).where(Notification.message_id == message_id)
        res = await self._execute(stmt)
        existing = set(res.scalars().all())

        missing = [user_id for user_id in unique_user_ids if user_id not in existing]
        if not missing:
            return

        stmt = insert(Notification).values(
            [{"message_id": message_id, "user_id": user_id} for user_id in missing]
        )
        await self._execute(stmt)

    async def hide(
        self,
        id: int,
        user_id: int,
    ) -> None:
        stmt = (
            update(Notification)
            .where(
                Notification.id == id,
                Notification.user_id == user_id,
            )
            .values(is_hidden=True)
            .returning(Notification.id)
        )

        res = await self._execute(stmt)
        if res.scalar_one_or_none() is None:
            raise ObjectNotFound(f"Notification with id {id} not found")

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[Notification]],
        **filters: Unpack[NotificationGetListFilters],
    ) -> Select[tuple[Notification]]:
        if (user_id := filters.get("user_id")) is not None:
            stmt = stmt.where(Notification.user_id == user_id)

        if (message_id := filters.get("message_id")) is not None:
            stmt = stmt.where(Notification.message_id == message_id)

        if filters.get("only_visible"):
            stmt = stmt.where(Notification.is_hidden.is_(False))

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[NotificationGetListFilters],
    ) -> list[NotificationResponse]:
        stmt = select(Notification).order_by(Notification.created_at.desc())

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._execute(stmt)

        return [
            NotificationResponse.model_validate(instance)
            for instance in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[NotificationGetListFilters],
    ) -> int:
        stmt = select(Notification)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._execute(stmt)

        return res.scalar_one()
