class AppException(Exception):
    pass


class ObjectAlreadyExists(AppException):
    pass


class ObjectNotFound(AppException):
    pass


class InvalidInput(AppException):
    pass


class Forbidden(AppException):
    pass


class Unauthorized(AppException):
    pass
