from typing import NotRequired, Required, Sequence, TypedDict

from ...enums.users import UserRole


class UserCreateParams(TypedDict):
    name: Required[str]
    surname: Required[str]
    patronymic: NotRequired[str | None]
    email: Required[str]
    role: Required[UserRole]
    is_admin: NotRequired[bool]


class UserUpdateParams(TypedDict):
    name: NotRequired[str]
    surname: NotRequired[str]
    patronymic: NotRequired[str | None]
    email: NotRequired[str]
    role: NotRequired[UserRole]
    is_admin: NotRequired[bool]


class UserLoginParams(TypedDict):
    email: Required[str]
    password: Required[str]


class UserGetListFilters(TypedDict):
    search_query: NotRequired[str]
    role: NotRequired[UserRole]
    is_admin: NotRequired[bool]
    ids: NotRequired[Sequence[int]]
