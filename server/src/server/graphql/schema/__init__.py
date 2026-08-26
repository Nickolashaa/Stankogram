import asyncio
from typing import AsyncGenerator

import strawberry

from ..context import AppInfo
from .auth.mutations import AuthMutation
from .auth.queries import AuthQuery
from .chats.mutations import ChatMutation
from .chats.queries import ChatQuery
from .messages.mutations import MessageMutation
from .messages.queries import MessageQuery


@strawberry.type
class Query(
    AuthQuery,
    ChatQuery,
    MessageQuery,
):
    @strawberry.field
    async def health() -> int:
        return 200


@strawberry.type
class Mutation(
    AuthMutation,
    ChatMutation,
    MessageMutation,
):
    pass


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def test(
        info: AppInfo,
        target: int,
    ) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(1)


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
