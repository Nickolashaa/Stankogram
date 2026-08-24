import strawberry

from ....enums.chats import ChatType

EChatType = strawberry.enum(ChatType, name="EChatType")
