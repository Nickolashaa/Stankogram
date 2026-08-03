from uuid import UUID

from sqlalchemy import exists, insert, select

from ..database.models.cancelled_jwt_tokens import CancelledRefreshToken
from .base import BaseService


class CancelledRefreshTokenService(BaseService):
    async def create(
        self,
        jti: UUID,
    ) -> None:
        stmt = insert(CancelledRefreshToken).values(jti=jti)
        await self._session.execute(stmt)

    async def is_exists(
        self,
        jti: UUID,
    ) -> bool:
        stmt = select(exists()).where(CancelledRefreshToken.jti == jti)
        res = await self._session.execute(stmt)
        return res.scalar_one()
