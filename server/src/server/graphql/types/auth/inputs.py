import strawberry

from ....services.auth.types import (
    UserCreateParams,
    UserCredentials,
    UserGetListFilters,
    UserUpdateParams,
)
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


@strawberry.input
class UserFiltersIn:
    search_query: strawberry.Maybe[str]
    role: strawberry.Maybe[EUserRole]
    is_admin: strawberry.Maybe[bool]

    def to_service_params(
        self,
    ) -> UserGetListFilters:
        filters: UserGetListFilters = {}
        if self.search_query is not None:
            filters["search_query"] = self.search_query.value
        if self.role is not None:
            filters["role"] = self.role.value
        if self.is_admin is not None:
            filters["is_admin"] = self.is_admin.value
        return filters
