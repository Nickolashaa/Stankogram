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
