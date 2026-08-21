from .auth import AuthService
from .base import Schema


class Services(Schema):
    auth_service: AuthService
