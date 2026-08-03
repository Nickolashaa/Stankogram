from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from ..database.models.cancelled_jwt_tokens import CancelledRefreshToken
from .base import BaseService
from .exceptions import ObjectAlreadyExists


class CancelledRefreshTokenService(BaseService):
    async def create(
        self,
        jti: UUID,
    ) -> None:
        stmt = insert(CancelledRefreshToken).values(jti=jti)
        try:
            await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(f"Token with jti {jti} already exists")
