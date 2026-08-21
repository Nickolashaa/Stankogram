import strawberry


@strawberry.type
class Query:
    @strawberry.field
    async def health() -> int:
        return 200


# @strawberry.type
# class Mutation:
#     pass


schema = strawberry.Schema(query=Query)
