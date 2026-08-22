import strawberry

from .auth.mutations import AuthMutation
from .auth.queries import AuthQuery


@strawberry.type
class Query(
    AuthQuery,
):
    @strawberry.field
    async def health() -> int:
        return 200


@strawberry.type
class Mutation(
    AuthMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
