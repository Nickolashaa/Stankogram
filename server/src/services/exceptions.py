from fastapi import HTTPException


class BaseException(Exception):
    http_code: int

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.http_code,
            detail=str(self),
        )


class ObjectAlreadyExists(BaseException):
    http_code = 422


class ObjectNotFound(BaseException):
    http_code = 404


class InvalidInput(BaseException):
    http_code = 422
