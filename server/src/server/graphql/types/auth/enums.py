import strawberry

from ....enums.users import UserRole

EUserRole = strawberry.enum(UserRole, name="EUserRole")
