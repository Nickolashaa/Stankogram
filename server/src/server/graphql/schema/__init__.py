import strawberry

from .auth.mutations import AuthMutation
from .auth.queries import AuthQuery
from .chats.mutations import ChatMutation
from .chats.queries import ChatQuery
from .events import EventSubscription
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
class Subscription(EventSubscription):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
