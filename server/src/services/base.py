from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.base import PaginationSchema


class BaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _apply_pagination[T](
        stmt: Select[tuple[T]],
        pagination: PaginationSchema | None,
    ) -> Select[tuple[T]]:
        if pagination is None:
            return stmt

        return stmt.limit(pagination.limit).offset(pagination.offset)
