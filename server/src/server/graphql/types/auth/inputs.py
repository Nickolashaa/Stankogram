import strawberry

from ....services.auth.types import UserCreateParams, UserCredentials, UserUpdateParams
from .enums import EUserRole


@strawberry.input
class UserIn:
    name: str
    surname: str
    patronymic: str | None
    email: str
    role: EUserRole
    is_admin: bool

    def to_service_params[T: (UserCreateParams, UserUpdateParams)](
        self, cls: type[T]
    ) -> T:
        return cls(
            name=self.name,
            surname=self.surname,
            patronymic=self.patronymic,
            email=self.email,
            role=self.role,
            is_admin=self.is_admin,
        )


@strawberry.input
class UserCredentialsIn:
    email: str
    password: str

    def to_service_params(
        self,
    ) -> UserCredentials:
        return UserCredentials(
            email=self.email,
            password=self.password,
        )
