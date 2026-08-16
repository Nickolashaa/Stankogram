from fastapi import HTTPException

from ..schemas.websockets import WebSocketError


class BaseException(Exception):
    code: int

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.code,
            detail=str(self),
        )

    def to_ws_exception(self) -> WebSocketError:
        return WebSocketError(code=self.code, message=str(self))


class ObjectAlreadyExists(BaseException):
    code = 422


class ObjectNotFound(BaseException):
    code = 404


class InvalidInput(BaseException):
    code = 422


class Forbidden(BaseException):
    code = 403
