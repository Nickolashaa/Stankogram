from typing import Union

import strawberry

from ...context import AppInfo
from ...types.auth import User
from ...types.errors import ObjectNotFoundError


@strawberry.type
class AuthQuery:
    @strawberry.field
    async def get_me(
        info: AppInfo,
    ) -> Union[User, ObjectNotFoundError]:
        current_user = info.context.current_user
        if current_user is None:
            return ObjectNotFoundError(message="User not found")
        return User.from_schema(current_user)
