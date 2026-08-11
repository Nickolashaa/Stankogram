from datetime import UTC, datetime, timedelta
from pathlib import Path
from secrets import choice
from string import Template, ascii_letters, digits

import bcrypt
from sqlalchemy import Select, delete, insert, or_, select, update
from sqlalchemy.exc import IntegrityError

from ...config import (
    APP_BASE_URL,
    PASSWORD_LEN,
    PASSWORD_RESET_CODE_EXP_MINUTES,
    PASSWORD_RESET_CODE_LEN,
)
from ...database.models.users import PasswordResetCode, User
from ...schemas.base import PaginationSchema
from ...schemas.users import (
    UserCredentials,
    UserFilters,
    UserInput,
    UserResponse,
)
from ...utils.smtp import send_email
from ...utils.stmt_modificators import _get_count_stmt
from ..base import BaseService
from ..exceptions import ObjectAlreadyExists, ObjectNotFound

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


class UserService(BaseService):
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
        url = f"{APP_BASE_URL}/api/users/{user_id}/reset_password_confirm/{code}"
        return _PASSWORD_RESET_EMAIL_TEMPLATE.substitute(url=url)

    @staticmethod
    def _generate_password_reset_confirm_email(email: str, password: str) -> str:
        return _PASSWORD_RESET_CONFIRM_EMAIL_TEMPLATE.substitute(
            email=email, password=password
        )

    async def create(
        self,
        data: UserInput,
    ) -> UserResponse:
        password = self._generate_password()
        hashed_password = bcrypt.hashpw(
            password=password.encode(), salt=bcrypt.gensalt()
        ).decode()

        stmt = (
            insert(User)
            .values(
                hashed_password=hashed_password,
                **data.model_dump(),
            )
            .returning(User)
        )

        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(f"User with email {data.email} already exists")

        await send_email(
            to_email=data.email,
            subject="Stankogram:Данные для входа",
            body=self._generate_create_email(email=data.email, password=password),
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
        filters: UserFilters | None,
    ) -> Select[tuple[User]]:
        if filters is None:
            return stmt

        if "search_query" in filters.model_fields_set:
            stmt = stmt.where(
                or_(
                    User.name.icontains(filters.search_query),
                    User.surname.icontains(filters.search_query),
                    User.patronymic.icontains(filters.search_query),
                    User.email.icontains(filters.search_query),
                )
            )

        if "role" in filters.model_fields_set:
            stmt = stmt.where(User.role == filters.role)

        if "is_admin" in filters.model_fields_set:
            stmt = stmt.where(User.is_admin == filters.is_admin)

        return stmt

    async def get_list(
        self,
        filters: UserFilters | None = None,
        pagination: PaginationSchema | None = None,
    ) -> list[UserResponse]:
        stmt = select(User).order_by(User.id)

        stmt = self._apply_filters(stmt=stmt, filters=filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)
        entities = res.scalars().all()

        return [UserResponse.model_validate(entity) for entity in entities]

    async def count(
        self,
        filters: UserFilters | None,
    ) -> int:
        stmt = select(User)

        stmt = self._apply_filters(stmt=stmt, filters=filters)

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
        credentials: UserCredentials,
    ) -> UserResponse:
        user = await self.get_by_email(credentials.email)

        if bcrypt.checkpw(credentials.password.encode(), user.hashed_password.encode()):
            return user

        raise ObjectNotFound(
            f"User with email {credentials.email} and password "
            f"{credentials.password} not found"
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
        data: UserInput,
    ) -> UserResponse:
        await self.get(id)

        stmt = (
            update(User)
            .where(User.id == id)
            .values(**data.model_dump())
            .returning(User)
        )

        try:
            res = await self._session.execute(stmt)
            return UserResponse.model_validate(res.scalar_one())
        except IntegrityError:
            raise ObjectAlreadyExists(f"User with email {data.email} already exists")

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
