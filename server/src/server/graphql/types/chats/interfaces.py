from typing import TYPE_CHECKING, Annotated

import strawberry

from ...context import AppInfo

if TYPE_CHECKING:
    from .types import Chat


@strawberry.interface
class IChat:
    chat_id: strawberry.Private[int]

    @strawberry.field
    async def chat(self, info: AppInfo) -> Annotated["Chat", strawberry.lazy(".types")]:
        return await info.context.data_loaders.chat_loader.load(self.chat_id)
