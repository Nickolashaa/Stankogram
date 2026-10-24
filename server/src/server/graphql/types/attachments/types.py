from typing import Self

import strawberry

from ....enums.attachments import AttachmentKind
from ....services.attachments.schemas import AttachmentResponse
from ....services.attachments.service import DEFAULT_CONTENT_TYPE
from ...context import AppInfo
from ..base import IBaseType
from .enums import EAttachmentKind


@strawberry.type
class Attachment(IBaseType):
    kind: EAttachmentKind
    name: str
    content_type: str
    size: int
    width: int | None
    height: int | None
    duration_ms: int | None
    key: strawberry.Private[str]
    thumbnail_key: strawberry.Private[str | None]

    def _attachment_url(self, info: AppInfo) -> str:
        return info.context.services.storage_service.download_url(
            self.key,
            name=self.name,
            content_type=(
                DEFAULT_CONTENT_TYPE if self.kind == AttachmentKind.FILE else None
            ),
        )

    @strawberry.field
    def url(self, info: AppInfo) -> str:
        if self.kind == AttachmentKind.FILE:
            return self._attachment_url(info)

        return info.context.services.storage_service.download_url(self.key)

    @strawberry.field
    def thumbnail_url(self, info: AppInfo) -> str | None:
        if self.thumbnail_key is None:
            return None

        return info.context.services.storage_service.download_url(self.thumbnail_key)

    @strawberry.field
    def download_url(self, info: AppInfo) -> str:
        return self._attachment_url(info)

    @classmethod
    def from_schema(cls, instance: AttachmentResponse) -> Self:
        return cls(
            id=instance.id,
            kind=instance.kind,
            name=instance.name,
            content_type=instance.content_type,
            size=instance.size,
            width=instance.width,
            height=instance.height,
            duration_ms=instance.duration_ms,
            key=instance.key,
            thumbnail_key=instance.thumbnail_key,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class AttachmentUpload:
    attachment: Attachment
    upload_url: str
    thumbnail_upload_url: str | None
