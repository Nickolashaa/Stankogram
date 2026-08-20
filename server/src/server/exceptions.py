class AppException(Exception):
    code: int


class ObjectAlreadyExists(AppException):
    code = 422


class ObjectNotFound(AppException):
    code = 404


class InvalidInput(AppException):
    code = 422


class Forbidden(AppException):
    code = 403


class Unauthorized(AppException):
    code = 401
