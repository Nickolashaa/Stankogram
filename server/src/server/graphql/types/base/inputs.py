import strawberry

from ....config import settings
from ....services.base import BasePagination


@strawberry.input
class BasePaginationIn:
    limit: int | None
    offset: int | None

    def to_service_params(self) -> BasePagination:
        return BasePagination(
            limit=self.limit,
            offset=self.offset,
        )


default_pagination = BasePaginationIn(
    limit=settings.LIMIT,
    offset=settings.OFFSET,
)
