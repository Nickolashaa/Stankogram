import strawberry

from ....enums.attachments import AttachmentKind

EAttachmentKind = strawberry.enum(AttachmentKind, name="EAttachmentKind")
