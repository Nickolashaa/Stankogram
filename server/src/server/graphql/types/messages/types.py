import strawberry

from ..auth import IUser
from ..base import IBaseType
from ..chats import IChat
from .enums import EMessageType


@strawberry.type
class Message(IBaseType, IUser, IChat):
    text: str
    type: EMessageType
