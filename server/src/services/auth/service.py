from datetime import UTC, datetime, timedelta
from pathlib import Path
from secrets import choice
from string import Template, ascii_letters, digits
from typing import Unpack
from uuid import UUID, uuid4

import bcrypt
from sqlalchemy import Select, delete, insert, or_, select, update
from sqlalchemy.exc import IntegrityError

from ...config import (
    APP_BASE_URL,
    JWT_ACCESS_EXP_MINUTES,
    JWT_REFRESH_EXP_DAYS,
    PASSWORD_LEN,
    PASSWORD_RESET_CODE_EXP_MINUTES,
    PASSWORD_RESET_CODE_LEN,
)
from ...database.models.auth import CancelledToken, PasswordResetCode, User
from ...schemas.jwt import JWTTokens, UserJWTPayload
from ...schemas.users import UserResponse
from ...utils.smtp import send_email
from ...utils.stmt_modificators import _get_count_stmt
from ..base import BaseService
from ..exceptions import ObjectAlreadyExists, ObjectNotFound
from .types import (
    UserCreateParams,
    UserGetListFilters,
    UserLoginParams,
    UserUpdateParams,
)

_CREATE_USER_EMAIL_TEMPLATE = Template(
    (Path(__file__).resolve().parent / "create_user_email.html").read_text(
        encoding="utf-8"
    )
)
_PASSWORD_RESET_EMAIL_TEMPLATE = Template(
    (Path(__file__).resolve().parent / "password_reset_email.html").read_text(
        encoding="utf-8"
    )
)
_PASSWORD_RESET_CONFIRM_EMAIL_TEMPLATE = Template(
    (Path(__file__).resolve().parent / "password_reset_confirm_email.html").read_text(
        encoding="utf-8"
    )
)


class AuthService(BaseService):
    @staticmethod
    def _generate_password() -> str:
        return "".join(choice(ascii_letters + digits) for _ in range(PASSWORD_LEN))

    @staticmethod
    def _generate_password_reset_code() -> str:
        return "".join(choice(digits) for _ in range(PASSWORD_RESET_CODE_LEN))

    @staticmethod
    def _generate_create_email(email: str, password: str) -> str:
        return _CREATE_USER_EMAIL_TEMPLATE.substitute(email=email, password=password)

    @staticmethod
    def _generate_password_reset_email(user_id: int, code: str) -> str:
        url = f"{APP_BASE_URL}/reset-password-confirm?id={user_id}&code={code}"
        return _PASSWORD_RESET_EMAIL_TEMPLATE.substitute(url=url)

    @staticmethod
    def _generate_password_reset_confirm_email(email: str, password: str) -> str:
        return _PASSWORD_RESET_CONFIRM_EMAIL_TEMPLATE.substitute(
            email=email, password=password
        )

    @staticmethod
    def generate_jwt_tokens(id: int, is_admin: bool) -> JWTTokens:
        return JWTTokens(
            access_token=UserJWTPayload(
                id=id,
                is_admin=is_admin,
                jti=str(uuid4()),
                type="access",
                exp=datetime.now(UTC) + timedelta(minutes=JWT_ACCESS_EXP_MINUTES),
            ).generate_token(),
            refresh_token=UserJWTPayload(
                id=id,
                is_admin=is_admin,
                jti=str(uuid4()),
                type="refresh",
                exp=datetime.now(UTC) + timedelta(days=JWT_REFRESH_EXP_DAYS),
            ).generate_token(),
        )

    async def cancel_token(self, jti: UUID) -> None:
        stmt = insert(CancelledToken).values(jti=jti)
        try:
            await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(f"Token with jti {jti} already exists")

    async def create(
        self,
        **values: Unpack[UserCreateParams],
    ) -> UserResponse:
        password = self._generate_password()
        hashed_password = bcrypt.hashpw(
            password=password.encode(), salt=bcrypt.gensalt()
        ).decode()

        stmt = (
            insert(User)
            .values(
                hashed_password=hashed_password,
                **values,
            )
            .returning(User)
        )

        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(
                f"User with email {values.get('email')} already exists"
            )

        await send_email(
            to_email=values.get("email"),
            subject="Stankogram:Данные для входа",
            body=self._generate_create_email(
                email=values.get("email"), password=password
            ),
        )

        return UserResponse.model_validate(res.scalar_one())

    async def get(
        self,
        id: int,
    ) -> UserResponse:
        stmt = select(User).where(User.id == id)
        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with id {id} not found",
            )
        return UserResponse.model_validate(entity)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[User]],
        **filters: Unpack[UserGetListFilters],
    ) -> Select[tuple[User]]:
        if (search_query := filters.get("search_query")) is not None:
            stmt = stmt.where(
                or_(
                    User.name.icontains(search_query),
                    User.surname.icontains(search_query),
                    User.patronymic.icontains(search_query),
                    User.email.icontains(search_query),
                )
            )

        if (role := filters.get("role")) is not None:
            stmt = stmt.where(User.role == role)

        if (is_admin := filters.get("is_admin")) is not None:
            stmt = stmt.where(User.is_admin == is_admin)

        return stmt

    async def get_list(
        self,
        limit: int | None,
        offset: int | None,
        **filters: Unpack[UserGetListFilters],
    ) -> list[UserResponse]:
        stmt = select(User).order_by(User.id)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = stmt.limit(limit).offset(offset)

        res = await self._session.execute(stmt)

        return [UserResponse.model_validate(entity) for entity in res.scalars().all()]

    async def count(
        self,
        **filters: Unpack[UserGetListFilters],
    ) -> int:
        stmt = select(User)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = _get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()

    async def get_by_email(
        self,
        email: str,
    ) -> UserResponse:
        stmt = select(User).where(User.email == email)
        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with email {email} not found",
            )
        return UserResponse.model_validate(entity)

    async def login(
        self,
        **credentials: Unpack[UserLoginParams],
    ) -> UserResponse:
        user = await self.get_by_email(credentials.get("email"))

        if bcrypt.checkpw(
            credentials.get("password").encode(), user.hashed_password.encode()
        ):
            return user

        raise ObjectNotFound(
            f"User with email {credentials.get('email')} and password "
            f"{credentials.get('password')} not found"
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(User).where(User.id == id)
        await self._session.execute(stmt)

    async def update(
        self,
        id: int,
        **values: Unpack[UserUpdateParams],
    ) -> UserResponse:
        await self.get(id)

        stmt = update(User).where(User.id == id).values(**values).returning(User)

        try:
            res = await self._session.execute(stmt)
            return UserResponse.model_validate(res.scalar_one())
        except IntegrityError:
            raise ObjectAlreadyExists(
                f"User with email {values.get('email')} already exists"
            )

    async def reset_password_request(
        self,
        email: str,
    ) -> None:
        user = await self.get_by_email(email)

        code = self._generate_password_reset_code()
        stmt = (
            insert(PasswordResetCode)
            .values(
                user_id=user.id,
                value=code,
            )
            .returning(PasswordResetCode)
        )

        await self._session.execute(stmt)

        await send_email(
            to_email=user.email,
            subject="Stankogram:Подтверждение сброса пароля",
            body=self._generate_password_reset_email(
                user_id=user.id,
                code=code,
            ),
        )

    async def reset_password_confirm(
        self,
        id: int,
        code: str,
    ) -> None:
        user = await self.get(id)

        stmt = select(PasswordResetCode).where(
            PasswordResetCode.user_id == user.id,
            PasswordResetCode.value == code,
            PasswordResetCode.created_at
            >= datetime.now(UTC) - timedelta(minutes=PASSWORD_RESET_CODE_EXP_MINUTES),
        )

        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"Valid password reset code for user {user.id} not found"
            )

        stmt = delete(PasswordResetCode).where(PasswordResetCode.id == entity.id)
        await self._session.execute(stmt)

        new_password = self._generate_password()
        new_hashed_password = bcrypt.hashpw(
            password=new_password.encode(), salt=bcrypt.gensalt()
        ).decode()

        stmt = (
            update(User)
            .where(User.id == id)
            .values(hashed_password=new_hashed_password)
        )
        await self._session.execute(stmt)

        await send_email(
            to_email=user.email,
            subject="Stankogram:Данные для входа",
            body=self._generate_password_reset_confirm_email(
                email=user.email,
                password=new_password,
            ),
        )
