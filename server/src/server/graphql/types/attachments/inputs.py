import strawberry

from ....services.attachments.types import AttachmentCreateParams


@strawberry.input
class AttachmentUploadIn:
    chat_id: int
    name: str
    content_type: str
    size: int
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None

    def to_create_service_params(self, user_id: int) -> AttachmentCreateParams:
        return AttachmentCreateParams(
            chat_id=self.chat_id,
            user_id=user_id,
            name=self.name,
            content_type=self.content_type,
            size=self.size,
            width=self.width,
            height=self.height,
            duration_ms=self.duration_ms,
        )
