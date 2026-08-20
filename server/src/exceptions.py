from fastapi import HTTPException

from .schemas.websockets import WebSocketError


class AppException(Exception):
    code: int

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.code,
            detail=str(self),
        )

    def to_ws_exception(self) -> WebSocketError:
        return WebSocketError(code=self.code, message=str(self))


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
