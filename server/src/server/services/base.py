from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import LIMIT, OFFSET


class BaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )


class PaginationSchema(Schema):
    limit: int | None = Field(LIMIT)
    offset: int | None = Field(OFFSET)


class BaseResponse(Schema):
    id: int
    created_at: datetime
    updated_at: datetime
