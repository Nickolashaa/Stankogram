from typing import Union, cast
from uuid import UUID

import jwt
import strawberry
from fastapi import UploadFile
from strawberry.file_uploads import Upload

from ....config import JWT_REFRESH_EXP_DAYS
from ....services.auth.schemas import JWTPayload
from ....services.exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ...context import AppInfo, AuthorizedAppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
from ...types.auth import (
    CreatedUser,
    JWTs,
    User,
    UserCredentialsIn,
    UserIn,
    UsersImportReport,
)
from ...types.errors import (
    InvalidInputError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
    UnauthorizedError,
)


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(
        self,
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
        self,
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
        self,
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

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsAdmin])
    async def user_create(
        self,
        info: AuthorizedAppInfo,
        input: UserIn,
    ) -> CreatedUser | ObjectAlreadyExistsError:
        try:
            instance = await info.context.services.auth_service.create(
                **input.to_create_service_params()
            )
            await info.context.session.commit()
            return CreatedUser.from_schema(instance)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsAdmin])
    async def users_import(
        self,
        info: AuthorizedAppInfo,
        file: Upload,
    ) -> UsersImportReport | InvalidInputError:
        try:
            report = await info.context.services.auth_service.import_users(
                content=await cast(UploadFile, file).read(),
            )
        except InvalidInput as e:
            return InvalidInputError.from_service_exception(e)

        return UsersImportReport.from_schema(report)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsAdmin])
    async def user_update(
        self,
        info: AuthorizedAppInfo,
        id: int,
        input: UserIn,
    ) -> User | ObjectAlreadyExistsError | ObjectNotFoundError:
        try:
            instance = await info.context.services.auth_service.update(
                id=id, **input.to_update_service_params()
            )
            await info.context.session.commit()
            return User.from_schema(instance)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsAdmin])
    async def user_delete(
        self,
        info: AuthorizedAppInfo,
        id: int,
    ) -> None:
        await info.context.services.auth_service.delete(id)
        await info.context.session.commit()

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def me_update_hide_last_online(
        self,
        info: AuthorizedAppInfo,
        hide_last_online: bool,
    ) -> User | ObjectNotFoundError:
        try:
            instance = await info.context.services.auth_service.update(
                id=info.context.current_user.id,
                hide_last_online=hide_last_online,
            )
            await info.context.session.commit()
            return User.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation
    async def user_reset_password_request(
        self, info: AppInfo, email: str
    ) -> None | ObjectNotFoundError:
        try:
            await info.context.services.auth_service.reset_password_request(email)
            await info.context.session.commit()
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation
    async def user_reset_password_confirm(
        self,
        info: AppInfo,
        id: int,
        code: str,
    ) -> None | ObjectNotFoundError:
        try:
            await info.context.services.auth_service.reset_password_confirm(
                id=id,
                code=code,
            )
            await info.context.session.commit()
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
