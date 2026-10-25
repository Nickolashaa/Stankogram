from typing import Union, cast
from uuid import UUID

import jwt
import strawberry
from fastapi import UploadFile
from strawberry.file_uploads import Upload

from ....config import settings
from ....enums.chats import ChatType
from ....enums.events import EventType
from ....enums.rate_limit import RateLimitScope
from ....services.attachments.schemas import AttachmentResponse
from ....services.attachments.service import AttachmentService
from ....services.auth.schemas import JWTPayload
from ....services.events.schemas import ChatParticipantEventSchema
from ....services.exceptions import (
    InvalidInput,
    ObjectAlreadyExists,
    ObjectNotFound,
    TooManyRequests,
)
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
    TooManyRequestsError,
    UnauthorizedError,
)


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(
        self,
        info: AppInfo,
        input: UserCredentialsIn,
    ) -> Union[JWTs, ObjectNotFoundError, TooManyRequestsError]:
        email_key = input.email.strip().lower()
        ip_key = info.context.client_ip

        rate_limit_service = info.context.services.rate_limit_service

        for scope, key in (
            (RateLimitScope.LOGIN_IP, ip_key),
            (RateLimitScope.LOGIN_EMAIL, email_key),
        ):
            if await rate_limit_service.is_blocked(scope, key):
                return TooManyRequestsError.after_seconds(
                    await rate_limit_service.retry_after_seconds(scope, key)
                )

        try:
            user = await info.context.services.auth_service.login(
                **input.to_service_params()
            )
        except ObjectNotFound as e:
            await rate_limit_service.hit(RateLimitScope.LOGIN_IP, ip_key)
            await rate_limit_service.hit(RateLimitScope.LOGIN_EMAIL, email_key)
            return ObjectNotFoundError.from_service_exception(e)

        await rate_limit_service.reset(RateLimitScope.LOGIN_EMAIL, email_key)

        tokens = info.context.services.auth_service.generate_jwts(
            id=user.id, is_admin=user.is_admin
        )

        info.context.response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path=settings.REFRESH_TOKEN_COOKIE_PATH,
            max_age=60 * 60 * 24 * settings.JWT_REFRESH_EXP_DAYS,
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

        info.context.response.delete_cookie(
            "refresh_token", path=settings.REFRESH_TOKEN_COOKIE_PATH
        )

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
            secure=True,
            samesite="lax",
            path=settings.REFRESH_TOKEN_COOKIE_PATH,
            max_age=60 * 60 * 24 * settings.JWT_REFRESH_EXP_DAYS,
        )

        return JWTs.from_schema(tokens)

    @strawberry.mutation
    async def logout(
        self,
        info: AppInfo,
    ) -> None:
        if info.context.refresh_token is None:
            return

        info.context.response.delete_cookie(
            "refresh_token", path=settings.REFRESH_TOKEN_COOKIE_PATH
        )

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
        services = info.context.services

        links = await services.chat_participant_service.get_list(user_id=id)

        recipient_ids: dict[int, list[int]] = {}
        orphaned: dict[int, AttachmentResponse] = {}

        for link in links:
            peers = await services.chat_participant_service.get_list(
                chat_id=link.chat_id,
                exclude_user_ids=[id],
            )
            recipient_ids[link.chat_id] = [peer.user_id for peer in peers]

            chat = await services.chat_service.get(link.chat_id)
            if chat.type == ChatType.PRIVATE or not peers:
                orphaned.update(
                    {
                        attachment.id: attachment
                        for attachment in await services.attachment_service.get_list(
                            chat_id=link.chat_id
                        )
                    }
                )

        orphaned.update(
            {
                attachment.id: attachment
                for attachment in await services.attachment_service.get_list(user_id=id)
            }
        )

        await services.chat_participant_service.purge_user(id)
        await services.auth_service.delete(id)
        await info.context.session.commit()

        await services.storage_service.delete(
            AttachmentService.object_keys(list(orphaned.values()))
        )

        for link in links:
            await services.event_service.publish(
                recipient_ids[link.chat_id],
                ChatParticipantEventSchema(
                    type=EventType.REMOVE_CHAT_PARTICIPANT,
                    participant=link,
                ),
            )

    @strawberry.mutation
    async def user_reset_password_request(
        self, info: AppInfo, email: str
    ) -> None | TooManyRequestsError:
        ip_key = info.context.client_ip

        rate_limit_service = info.context.services.rate_limit_service

        if await rate_limit_service.is_blocked(
            RateLimitScope.PASSWORD_RESET_REQUEST, ip_key
        ):
            return TooManyRequestsError.after_seconds(
                await rate_limit_service.retry_after_seconds(
                    RateLimitScope.PASSWORD_RESET_REQUEST, ip_key
                )
            )

        await rate_limit_service.hit(RateLimitScope.PASSWORD_RESET_REQUEST, ip_key)

        try:
            await info.context.services.auth_service.reset_password_request(
                email=email,
                codes=info.context.services.password_reset_service,
            )
            await info.context.session.commit()
        except TooManyRequests as e:
            await info.context.session.rollback()
            return TooManyRequestsError.from_service_exception(e)

    @strawberry.mutation
    async def user_reset_password_confirm(
        self,
        info: AppInfo,
        id: int,
        code: str,
    ) -> None | ObjectNotFoundError | TooManyRequestsError:
        ip_key = info.context.client_ip

        rate_limit_service = info.context.services.rate_limit_service

        if await rate_limit_service.is_blocked(
            RateLimitScope.PASSWORD_RESET_CONFIRM, ip_key
        ):
            return TooManyRequestsError.after_seconds(
                await rate_limit_service.retry_after_seconds(
                    RateLimitScope.PASSWORD_RESET_CONFIRM, ip_key
                )
            )

        await rate_limit_service.hit(RateLimitScope.PASSWORD_RESET_CONFIRM, ip_key)

        try:
            await info.context.services.auth_service.reset_password_confirm(
                id=id,
                code=code,
                codes=info.context.services.password_reset_service,
            )
            await info.context.session.commit()
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
