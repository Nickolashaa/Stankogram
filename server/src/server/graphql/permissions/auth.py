from typing import Any

from strawberry.permission import BasePermission

from ..context import AppInfo


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(
        self,
        source: Any,
        info: AppInfo,
        **kwargs,
    ) -> bool:
        return info.context.current_user is not None
