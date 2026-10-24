import re
from collections.abc import Sequence
from typing import Unpack
from uuid import uuid4

from sqlalchemy import Select, delete, insert, select, update

from ...config import settings
from ...database.models.attachments import Attachment
from ...enums.attachments import AttachmentKind
from ..base import BaseService
from ..exceptions import InvalidInput
from .schemas import AttachmentResponse
from .types import AttachmentCreateParams, AttachmentGetListFilters

CONTENT_TYPES = {
    AttachmentKind.IMAGE: frozenset(
        {"image/jpeg", "image/png", "image/webp", "image/gif"}
    ),
    AttachmentKind.VIDEO: frozenset({"video/mp4", "video/webm", "video/quicktime"}),
}

CONTENT_TYPE_PATTERN = re.compile(r"^[\w.+-]+/[\w.+-]+$")
CONTENT_TYPE_MAX_LEN = 255
DEFAULT_CONTENT_TYPE = "application/octet-stream"

MAX_SIZES = {
    AttachmentKind.IMAGE: settings.ATTACHMENT_MAX_IMAGE_SIZE,
    AttachmentKind.VIDEO: settings.ATTACHMENT_MAX_VIDEO_SIZE,
    AttachmentKind.FILE: settings.ATTACHMENT_MAX_FILE_SIZE,
}

THUMBNAIL_KINDS = frozenset({AttachmentKind.IMAGE, AttachmentKind.VIDEO})

THUMBNAIL_CONTENT_TYPE = "image/jpeg"


class AttachmentService(BaseService):
    @staticmethod
    def get_content_type(content_type: str) -> str:
        value = content_type.strip().lower()
        if value == "":
            return DEFAULT_CONTENT_TYPE

        if (
            len(value) > CONTENT_TYPE_MAX_LEN
            or CONTENT_TYPE_PATTERN.match(value) is None
        ):
            raise InvalidInput(f"Malformed attachment type {content_type}")

        return value

    @staticmethod
    def get_kind(content_type: str) -> AttachmentKind:
        for kind, content_types in CONTENT_TYPES.items():
            if content_type in content_types:
                return kind

        return AttachmentKind.FILE

    @staticmethod
    def get_max_size(kind: AttachmentKind) -> int:
        return MAX_SIZES[kind]

    async def create(
        self,
        **values: Unpack[AttachmentCreateParams],
    ) -> AttachmentResponse:
        values["content_type"] = self.get_content_type(values["content_type"])
        kind = self.get_kind(values["content_type"])
        max_size = self.get_max_size(kind)
        if values["size"] <= 0 or values["size"] > max_size:
            raise InvalidInput(
                f"Attachment size must be between 1 and {max_size} bytes"
            )

        token = uuid4().hex
        key = f"chats/{values['chat_id']}/{token}"
        stmt = (
            insert(Attachment)
            .values(
                kind=kind,
                key=key,
                thumbnail_key=(f"{key}_thumb" if kind in THUMBNAIL_KINDS else None),
                **values,
            )
            .returning(Attachment)
        )

        res = await self._execute(stmt)

        return AttachmentResponse.model_validate(res.scalar_one())

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[Attachment]],
        **filters: Unpack[AttachmentGetListFilters],
    ) -> Select[tuple[Attachment]]:
        if (ids := filters.get("ids")) is not None:
            stmt = stmt.where(Attachment.id.in_(ids))

        if (chat_id := filters.get("chat_id")) is not None:
            stmt = stmt.where(Attachment.chat_id == chat_id)

        if (user_id := filters.get("user_id")) is not None:
            stmt = stmt.where(Attachment.user_id == user_id)

        if (message_id := filters.get("message_id")) is not None:
            stmt = stmt.where(Attachment.message_id == message_id)

        if (message_ids := filters.get("message_ids")) is not None:
            stmt = stmt.where(Attachment.message_id.in_(message_ids))

        if (is_attached := filters.get("is_attached")) is not None:
            stmt = stmt.where(
                Attachment.message_id.is_not(None)
                if is_attached
                else Attachment.message_id.is_(None)
            )

        return stmt

    async def get_list(
        self,
        **filters: Unpack[AttachmentGetListFilters],
    ) -> list[AttachmentResponse]:
        stmt = self._apply_filters(select(Attachment), **filters)
        stmt = stmt.order_by(Attachment.id)

        res = await self._execute(stmt)

        return [
            AttachmentResponse.model_validate(instance)
            for instance in res.scalars().all()
        ]

    async def attach(
        self,
        ids: list[int],
        message_id: int,
        sizes: dict[int, int],
    ) -> list[AttachmentResponse]:
        instances = []

        for id in ids:
            stmt = (
                update(Attachment)
                .where(Attachment.id == id)
                .values(message_id=message_id, size=sizes[id])
                .returning(Attachment)
            )
            res = await self._execute(stmt)
            instances.append(AttachmentResponse.model_validate(res.scalar_one()))

        return instances

    @staticmethod
    def object_keys(instances: Sequence[AttachmentResponse]) -> list[str]:
        return [
            key
            for instance in instances
            for key in (instance.key, instance.thumbnail_key)
            if key is not None
        ]

    async def delete(self, ids: list[int]) -> None:
        if not ids:
            return

        await self._execute(delete(Attachment).where(Attachment.id.in_(ids)))
