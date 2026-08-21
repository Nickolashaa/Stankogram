import strawberry

from ....config import LIMIT, OFFSET
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
    limit=LIMIT,
    offset=OFFSET,
)
