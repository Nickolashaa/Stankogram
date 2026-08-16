from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from ..dependencies import (
    get_current_user_ws,
    get_websocket_connection_manager,
)
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
    await manager.connect(
        websocket=websocket,
        user_id=user.id,
    )

    try:
        while True:
            try:
                data = WebSocketSchemaAdapter.validate_python(
                    await websocket.receive_json()
                )
            except ValidationError:
                await websocket.send_json(
                    data=WebSocketError(
                        code=422,
                        message="Validation failed",
                    ).model_dump(),
                )
                continue

            await manager.process_event(
                data=data,
                user=user,
            )

    except WebSocketDisconnect:
        await manager.disconnect(user_id=user.id)
