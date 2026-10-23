from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import strawberry

from ...database.connection import session_maker
from ...dependencies.auth import get_user_from_authorization
from ...services.auth import AuthService
from ..context import AppInfo
from ..types.messages import Event, event_from_schema


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

        try:
            async with info.context.services.presence_service.track(user.id):
                async for event in info.context.services.event_service.listen(user.id):
                    yield event_from_schema(event)
        finally:
            await _save_last_online(user.id)
