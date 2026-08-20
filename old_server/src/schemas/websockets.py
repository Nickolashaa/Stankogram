from fastapi import WebSocket
from pydantic import TypeAdapter

from .base import Schema
from .messages import MessageCreate


class WebSocketError(Schema):
    code: int
    message: str


WebSocketSchema = MessageCreate | WebSocketError
WebSocketSchemaAdapter: TypeAdapter[WebSocketSchema] = TypeAdapter(WebSocketSchema)


class ActiveConnection(Schema):
    user_id: int
    websocket: WebSocket
