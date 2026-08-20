from cryptography.fernet import Fernet
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from ..config import ENCRYPTION_KEY
from ..dependencies import get_connection_registry, get_session
from ..exceptions import AppException, ObjectNotFound, Unauthorized
from ..schemas.websockets import WebSocketError, WebSocketSchemaAdapter
from ..services import (
    AuthService,
    ChatManager,
    ChatParticipantService,
    MessageService,
    PrivateChatService,
    PublicChatProfileService,
    WebSocketConnectionManager,
)

router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(),
) -> None:
    connection_registry = get_connection_registry()

    try:
        async with get_session() as session:
            auth_service = AuthService(session)
            user = await auth_service.get_from_token(token)
    except (Unauthorized, ObjectNotFound) as e:
        raise e.to_http_exception()

    await websocket.accept()
    connection_registry.add(
        user_id=user.id,
        websocket=websocket,
    )

    try:
        while True:
            try:
                data = WebSocketSchemaAdapter.validate_python(
                    await websocket.receive_json()
                )
            except ValidationError:
                await websocket.send_json(
                    WebSocketError(
                        code=422,
                        message="Validation failed",
                    ).model_dump(),
                )
                continue

            try:
                async with get_session() as session:
                    manager = WebSocketConnectionManager(
                        connection_registry=connection_registry,
                        chat_manager=ChatManager(
                            session=session,
                            private_chat_service=PrivateChatService(session),
                            public_chat_profile_service=PublicChatProfileService(
                                session
                            ),
                            message_service=MessageService(
                                session=session, fernet=Fernet(ENCRYPTION_KEY)
                            ),
                            auth_service=AuthService(session),
                            chat_participant_service=ChatParticipantService(session),
                        ),
                    )
                    await manager.process_event(
                        data=data,
                        user=user,
                    )
            except AppException as e:
                await websocket.send_json(e.to_ws_exception().model_dump())

    except WebSocketDisconnect:
        pass
    finally:
        connection_registry.remove(user.id)
