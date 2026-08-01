from random import choices
from string import ascii_letters, digits

import bcrypt
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from ..config import MIN_PASSWORD_LEN
from ..database.models.users import User
from ..schemas.users import UserCreate, UserCredentials, UserResponse
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
        return "".join(
            choices(
                population=ascii_letters + digits,
                k=MIN_PASSWORD_LEN,
            )
        )

    async def register(
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
