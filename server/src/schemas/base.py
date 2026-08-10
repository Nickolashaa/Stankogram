from pydantic import BaseModel, ConfigDict, Field

from ..config import LIMIT, OFFSET


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class HealthResponse(BaseModel):
    code: int
    message: str


class PaginationSchema(Schema):
    limit: int | None = Field(LIMIT)
    offset: int | None = Field(OFFSET)
