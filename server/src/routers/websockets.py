from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from ..dependencies import (
    get_current_user_ws,
    get_websocket_connection_manager,
)
from ..exceptions import AppException
from ..schemas.users import UserResponse
from ..schemas.websockets import WebSocketError, WebSocketSchemaAdapter
from ..services.websockets import WebSocketConnectionManager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: UserResponse = Depends(get_current_user_ws),
    manager: WebSocketConnectionManager = Depends(get_websocket_connection_manager),
) -> None:
    try:
        await manager.connect(
            websocket=websocket,
            user_id=user.id,
        )

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
                await manager.process_event(
                    data=data,
                    user=user,
                )
            except AppException as e:
                await websocket.send_json(e.to_ws_exception().model_dump())

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(user_id=user.id)
