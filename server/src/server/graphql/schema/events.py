from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import strawberry

from ...database.connection import session_maker
from ...dependencies.auth import get_user_from_authorization
from ...services.auth import AuthService
from ..context import AppInfo
from ..pubsub import pub_sub
from ..types.messages import CreateMessage, DeleteMessage, UpdateMessage

Event = CreateMessage | UpdateMessage | DeleteMessage


async def _save_last_online(user_id: int) -> None:
    async with session_maker() as session:
        await AuthService(session).update(
            id=user_id,
            last_online_at=datetime.now(UTC),
        )
        await session.commit()


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
            if pub_sub.disconnect(user.id, queue):
                await _save_last_online(user.id)
