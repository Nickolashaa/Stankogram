from typing import Self

import strawberry

from ....services.exceptions import AppException


@strawberry.interface
class IAppError:
    message: str

    @classmethod
    def from_service_exception(cls, instance: AppException) -> Self:
        return cls(message=str(instance))
