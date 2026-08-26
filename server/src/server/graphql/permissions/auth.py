from typing import Any

from strawberry.permission import BasePermission

from ..context import AuthorizedAppInfo


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: AuthorizedAppInfo, **kwargs) -> bool:
        return getattr(info.context, "current_user", None) is not None


class IsAdmin(BasePermission):
    message = "User is not admin"

    def has_permission(self, source: Any, info: AuthorizedAppInfo, **kwargs) -> bool:
        current_user = getattr(info.context, "current_user", None)
        return current_user is not None and current_user.is_admin is True
