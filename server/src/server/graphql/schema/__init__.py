import strawberry

from .auth.mutations import AuthMutation
from .auth.queries import AuthQuery
from .chats.mutations import ChatMutation
from .chats.queries import ChatQuery
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
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
