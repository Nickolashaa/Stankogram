import strawberry

from ...context import AppInfo
from .types import User


@strawberry.interface
class IUser:
    user_id: strawberry.Private[int]

    @strawberry.field
    async def user(self, info: AppInfo) -> User:
        return await info.context.data_loaders.user_loader.load(key=self.user_id)
