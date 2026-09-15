import strawberry

from .auth.mutations import AuthMutation
from .auth.queries import AuthQuery
from .chats.mutations import ChatMutation
from .chats.queries import ChatQuery
from .events import EventSubscription
from .messages.mutations import MessageMutation
from .messages.queries import MessageQuery
from .notifications.mutations import NotificationMutation
from .notifications.queries import NotificationQuery
from .system_notifications.mutations import SystemNotificationMutation
from .system_notifications.queries import SystemNotificationQuery


@strawberry.type
class Query(
    AuthQuery,
    ChatQuery,
    MessageQuery,
    NotificationQuery,
    SystemNotificationQuery,
):
    @strawberry.field
    async def health() -> int:
        return 200


@strawberry.type
class Mutation(
    AuthMutation,
    ChatMutation,
    MessageMutation,
    NotificationMutation,
    SystemNotificationMutation,
):
    pass


@strawberry.type
class Subscription(EventSubscription):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
