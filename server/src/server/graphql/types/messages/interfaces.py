from typing import TYPE_CHECKING, Annotated

import strawberry

from ...context import AppInfo

if TYPE_CHECKING:
    from .types import Message


@strawberry.interface
class IMessage:
    message_id: strawberry.Private[int]

    @strawberry.field
    async def message(
        self, info: AppInfo
    ) -> Annotated["Message", strawberry.lazy(".types")]:
        return await info.context.data_loaders.message_loader.load(self.message_id)
