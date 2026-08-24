from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[Any]],
        pagination: BasePagination | None,
    ) -> Select[tuple[Any]]:
        if pagination is None:
            return stmt
        return stmt.limit(pagination.limit).offset(pagination.offset)

    @staticmethod
    def _get_count_stmt(stmt: Select[tuple[Any]]) -> Select[tuple[int]]:
        return select(func.count()).select_from(stmt.subquery())


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )


class BasePagination(Schema):
    limit: int | None
    offset: int | None


class BaseResponse(Schema):
    id: int
    created_at: datetime
    updated_at: datetime
