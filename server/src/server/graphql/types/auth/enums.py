import strawberry

from ....enums.users import UserOnlineStatus, UserRole

EUserRole = strawberry.enum(UserRole, name="EUserRole")

EUserOnlineStatus = strawberry.enum(UserOnlineStatus, name="EUserOnlineStatus")
