import strawberry

from .auth.queries import AuthQuery


@strawberry.type
class Query(
    AuthQuery,
):
    @strawberry.field
    async def health() -> int:
        return 200


# @strawberry.type
# class Mutation:
#     pass


schema = strawberry.Schema(query=Query)
