from strawberry.fastapi import GraphQLRouter

from .context import Context
from .context_getter import context_getter
from .schema import schema

graphql_router = GraphQLRouter[Context, None](
    schema=schema, context_getter=context_getter
)
