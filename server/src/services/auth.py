from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from ..config import JWT_ACCESS_EXP_MINUTES, JWT_REFRESH_EXP_DAYS
from ..database.models.auth import CancelledToken
from ..schemas.jwt import JWTTokens, UserJWTPayload
from ..schemas.users import UserResponse
from .base import BaseService
from .exceptions import ObjectAlreadyExists


class AuthService(BaseService):
    @staticmethod
    def generate_jwt_tokens(user: UserResponse) -> JWTTokens:
        return JWTTokens(
            access_token=UserJWTPayload(
                id=user.id,
                is_admin=user.is_admin,
                jti=str(uuid4()),
                type="access",
                exp=datetime.now(timezone.utc)
                + timedelta(minutes=JWT_ACCESS_EXP_MINUTES),
            ).generate_token(),
            refresh_token=UserJWTPayload(
                id=user.id,
                is_admin=user.is_admin,
                jti=str(uuid4()),
                type="refresh",
                exp=datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXP_DAYS),
            ).generate_token(),
        )

    async def cancel_token(self, jti: UUID) -> None:
        stmt = insert(CancelledToken).values(jti=jti)
        try:
            await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectAlreadyExists(f"Token with jti {jti} already exists")
