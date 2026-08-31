from typing import Unpack

from sqlalchemy import Select, insert, select, update
from sqlalchemy.exc import IntegrityError

from ...database.models.system_notifications import (
    ReadSystemNotification,
    SystemNotification,
)
from ..base import BasePagination, BaseService
from ..exceptions import ObjectAlreadyExists, ObjectNotFound
from .schemas import SystemNotificationResponse
from .types import (
    SystemNotificationCreateParams,
    SystemNotificationGetListFilters,
    SystemNotificationUpdateParams,
)


class SystemNotificationService(BaseService):
    async def create(
        self,
        **data: Unpack[SystemNotificationCreateParams],
    ) -> SystemNotificationResponse:
        stmt = insert(SystemNotification).values(**data).returning(SystemNotification)

        res = await self._session.execute(stmt)

        return SystemNotificationResponse.model_validate(res.scalar_one())

    async def update(
        self,
        id: int,
        **values: Unpack[SystemNotificationUpdateParams],
    ) -> SystemNotificationResponse:
        stmt = (
            update(SystemNotification)
            .where(SystemNotification.id == id)
            .values(**values)
            .returning(SystemNotification)
        )

        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"System notification with id {id} not found",
            )
        return SystemNotificationResponse.model_validate(entity)

    async def mark_as_read(
        self,
        id: int,
        user_id: int,
    ) -> None:
        stmt = insert(ReadSystemNotification).values(
            system_notification_id=id,
            user_id=user_id,
        )

        try:
            await self._session.execute(stmt)
        except IntegrityError as e:
            if "uq_user_system_notification" in str(e.orig):
                raise ObjectAlreadyExists(
                    f"System notification with id {id} already read",
                )
            if "fk_read_system_notifications_system_notification_id" in str(e.orig):
                raise ObjectNotFound(
                    f"System notification with id {id} not found",
                )
            if "fk_read_system_notifications_user_id" in str(e.orig):
                raise ObjectNotFound(
                    f"User with id {user_id} not found",
                )
            raise

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[SystemNotification]],
        **filters: Unpack[SystemNotificationGetListFilters],
    ) -> Select[tuple[SystemNotification]]:
        if (unread_by_user_id := filters.get("unread_by_user_id")) is not None:
            stmt = stmt.where(
                ~select(ReadSystemNotification.id)
                .where(
                    ReadSystemNotification.system_notification_id
                    == SystemNotification.id,
                    ReadSystemNotification.user_id == unread_by_user_id,
                )
                .exists()
            )

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[SystemNotificationGetListFilters],
    ) -> list[SystemNotificationResponse]:
        stmt = select(SystemNotification).order_by(SystemNotification.created_at)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            SystemNotificationResponse.model_validate(instance)
            for instance in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[SystemNotificationGetListFilters],
    ) -> int:
        stmt = select(SystemNotification)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
