from typing import Union
from uuid import UUID

import jwt
import strawberry

from ....config import JWT_REFRESH_EXP_DAYS
from ....services.auth.schemas import JWTPayload
from ....services.exceptions import ObjectAlreadyExists, ObjectNotFound
from ...context import AppInfo
from ...types.auth import JWTs, UserCredentialsIn
from ...types.errors import (
    ObjectNotFoundError,
    UnauthorizedError,
)


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

    @strawberry.mutation
    async def refresh(
        info: AppInfo,
    ) -> Union[JWTs, UnauthorizedError, ObjectNotFoundError]:
        if info.context.refresh_token is None:
            return ObjectNotFoundError(message="Refresh token not found")

        try:
            payload = JWTPayload.from_token(info.context.refresh_token)
        except jwt.ExpiredSignatureError:
            return UnauthorizedError(message="Expired token")
        except jwt.InvalidTokenError:
            return UnauthorizedError(message="Invalid token")

        if payload.type != "refresh":
            return UnauthorizedError(message="Invalid token type")

        info.context.response.delete_cookie("refresh_token")

        try:
            await info.context.services.auth_service.cancel_token(UUID(payload.jti))
        except ObjectAlreadyExists:
            return UnauthorizedError(message="Token in blacklist")

        try:
            user = await info.context.services.auth_service.get(payload.id)
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

    @strawberry.mutation
    async def logout(
        info: AppInfo,
    ) -> None:
        if info.context.refresh_token is None:
            return

        info.context.response.delete_cookie("refresh_token")

        try:
            payload = JWTPayload.from_token(info.context.refresh_token)
            await info.context.services.auth_service.cancel_token(UUID(payload.jti))
        except Exception:
            pass
