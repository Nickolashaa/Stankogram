from secrets import choice
from string import ascii_letters, digits

import bcrypt
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import Select, insert, or_, select
from sqlalchemy.exc import IntegrityError

from ..config import MIN_PASSWORD_LEN
from ..database.models.users import User
from ..schemas.users import (
    UserCreate,
    UserCredentials,
    UserFilters,
    UserResponse,
)
from ..utils.stmt_modificators import _get_count_stmt
from ..utils.transliteration import transliterate
from .base import BaseService
from .exceptions import ObjectAlreadyExists, ObjectNotFound


class UserService(BaseService):
    @staticmethod
    def _generate_login(
        name: str,
        surname: str,
        patronymic: str | None,
        salt_number: int | None,
    ) -> str:
        return (
            f"{transliterate(surname).capitalize()}"
            f"{transliterate(name[0]).upper()}"
            f"{transliterate(patronymic[0]).upper() if patronymic is not None else ''}"
            f"{salt_number if salt_number is not None else ''}"
        )

    @staticmethod
    def _generate_password() -> str:
        return "".join(choice(ascii_letters + digits) for _ in range(MIN_PASSWORD_LEN))

    async def create(
        self,
        payload: UserCreate,
    ) -> UserCredentials:
        salt_number = None
        password = self._generate_password()
        hashed_password = bcrypt.hashpw(
            password=password.encode(), salt=bcrypt.gensalt()
        ).decode()
        while True:
            login = self._generate_login(
                name=payload.name,
                surname=payload.surname,
                patronymic=payload.patronymic,
                salt_number=salt_number,
            )
            try:
                stmt = insert(User).values(
                    login=login,
                    hashed_password=hashed_password,
                    **payload.model_dump(),
                )
                await self._session.execute(stmt)
                return UserCredentials(
                    login=login,
                    password=password,
                )
            except IntegrityError as e:
                await self._session.rollback()
                assert e.orig is not None
                cause = e.orig.__cause__
                if isinstance(cause, UniqueViolationError):
                    match cause.constraint_name:
                        case "uq_users_login":
                            if salt_number is None:
                                salt_number = 0
                            else:
                                salt_number += 1
                            continue
                        case "uq_users_phone_number":
                            raise ObjectAlreadyExists(
                                f"User with phone number {payload.phone_number} "
                                "already exists"
                            )
                raise

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
                    User.login.icontains(filters.search_query),
                    User.phone_number.icontains(filters.search_query),
                )
            )

        if "role" in filters.model_fields_set:
            stmt = stmt.where(User.role == filters.role)

        if "is_admin" in filters.model_fields_set:
            stmt = stmt.where(User.is_admin == filters.is_admin)

        return stmt

    async def get_list(
        self,
        filters: UserFilters | None,
        limit: int | None,
        offset: int | None,
    ) -> list[UserResponse]:
        stmt = select(User).order_by(User.id)

        stmt = self._apply_filters(stmt=stmt, filters=filters)

        stmt = stmt.limit(limit).offset(offset)

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

    async def get_by_login(
        self,
        login: str,
    ) -> UserResponse:
        stmt = select(User).where(User.login == login)
        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"User with login {login} not found",
            )
        return UserResponse.model_validate(entity)

    async def login(
        self,
        credentials: UserCredentials,
    ) -> UserResponse:
        user = await self.get_by_login(credentials.login)

        if bcrypt.checkpw(credentials.password.encode(), user.hashed_password.encode()):
            return user

        raise ObjectNotFound(
            f"User with login {credentials.login} and password "
            f"{credentials.password} not found"
        )
