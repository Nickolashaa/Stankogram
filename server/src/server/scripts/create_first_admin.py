import asyncio

from sqlalchemy import select

from ..database.connection import session_maker
from ..database.models.auth import User
from ..enums.users import UserRole
from ..services.auth import AuthService


async def main() -> None:
    async with session_maker() as session:
        existing = await session.execute(select(User).where(User.is_admin.is_(True)))
        if existing.scalar_one_or_none() is not None:
            print("Admin already exists, aborting.")
            return

        service = AuthService(session)
        await service.create(
            name=input("Name: "),
            surname=input("Surname: "),
            patronymic=input("Patronymic: "),
            email=input("Email: "),
            role=UserRole.STUDENT,
            is_admin=True,
        )
        await session.commit()

    print("Success, credentials sended in your email.")


asyncio.run(main())
