from math import ceil
from typing import Self

import strawberry

from .interfaces import IAppError


@strawberry.type
class ObjectNotFoundError(IAppError):
    pass


@strawberry.type
class ObjectAlreadyExistsError(IAppError):
    pass


@strawberry.type
class InvalidInputError(IAppError):
    pass


@strawberry.type
class ForbiddenError(IAppError):
    pass


@strawberry.type
class UnauthorizedError(IAppError):
    pass


@strawberry.type
class TooManyRequestsError(IAppError):
    @classmethod
    def after_seconds(cls, seconds: int) -> Self:
        minutes = ceil(seconds / 60)
        return cls(message=f"Слишком много попыток. Повторите через {minutes} мин")
