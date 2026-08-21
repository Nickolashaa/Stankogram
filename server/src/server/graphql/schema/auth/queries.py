from typing import Union

import strawberry

from ...context import AppInfo
from ...permissions.auth import IsAuthenticated
from ...types.auth import User, UserFiltersIn, UsersMeta
from ...types.base import BasePaginationIn, default_pagination
from ...types.errors import ObjectNotFoundError


@strawberry.type
class AuthQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_me(
        info: AppInfo,
    ) -> Union[User, ObjectNotFoundError]:
        current_user = info.context.current_user
        if current_user is None:
            return ObjectNotFoundError(message="User not found")
        return User.from_schema(current_user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_users(
        info: AppInfo,
        pagination: BasePaginationIn | None = None,
        filters: UserFiltersIn | None = None,
    ) -> UsersMeta:
        return UsersMeta(
            users=[
                User.from_schema(instance)
                for instance in await info.context.services.auth_service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    **filters.to_service_params() if filters is not None else {},
                )
            ],
            count=await info.context.services.auth_service.count(
                **filters.to_service_params() if filters is not None else {}
            ),
        )
