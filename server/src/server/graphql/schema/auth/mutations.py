from typing import Union

import strawberry

from ....config import JWT_REFRESH_EXP_DAYS
from ....services.exceptions import ObjectNotFound
from ...context import AppInfo
from ...types.auth import JWTs, UserCredentialsIn
from ...types.errors import ObjectNotFoundError


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(
        info: AppInfo,
        input: UserCredentialsIn,
    ) -> Union[JWTs, ObjectNotFoundError]:
        try:
            user = await info.context.services.auth_service.login(
                **input.to_service_params()
            )
        except ObjectNotFound as e:
            return ObjectNotFoundError.from_service_exception(e)

        tokens = info.context.services.auth_service.generate_jwts(
            id=user.id, is_admin=user.is_admin
        )

        info.context.response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * JWT_REFRESH_EXP_DAYS,
        )

        return JWTs.from_schema(tokens)
