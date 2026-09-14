from base64 import b64encode
from typing import Self

import strawberry

from ....services.base import XlsxFileSchema


@strawberry.type
class XlsxFile:
    filename: str
    content: str

    @classmethod
    def from_schema(cls, instance: XlsxFileSchema) -> Self:
        return cls(
            filename=instance.filename,
            content=b64encode(instance.content).decode(),
        )
