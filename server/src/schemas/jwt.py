from .base import Schema


class JWTTokens(Schema):
    access_token: str
    refresh_token: str
