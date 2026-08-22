import strawberry

from ...context import AppInfo
from .types import Chat


@strawberry.interface
class IChat:
    chat_id: strawberry.Private[int]

    @strawberry.field
    async def chat(self, info: AppInfo) -> Chat:
        return await info.context.data_loaders.chat_loader.load(self.chat_id)
