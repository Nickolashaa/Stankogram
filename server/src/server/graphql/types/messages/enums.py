import strawberry

from ....enums.messages import MessageType

EMessageType = strawberry.enum(MessageType, name="EMessageType")
