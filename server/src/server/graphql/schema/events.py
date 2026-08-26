from typing import AsyncGenerator

import strawberry

from ...dependencies.auth import get_user_from_authorization
from ..context import AppInfo
from ..pubsub import Event, pub_sub


@strawberry.type
class EventSubscription:
    @strawberry.subscription
    async def events(info: AppInfo) -> AsyncGenerator[Event, None]:
        connection_params = info.context.connection_params or {}
        user = await get_user_from_authorization(
            connection_params.get("Authorization"),
            info.context.services.auth_service,
        )
        if user is None:
            raise Exception("User is not authenticated")

        queue = pub_sub.connect(user.id)
        try:
            while True:
                event = await queue.get()
                if event is None:
                    return
                yield event
        finally:
            pub_sub.disconnect(user.id, queue)
