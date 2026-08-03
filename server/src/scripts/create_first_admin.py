import asyncio
import os

from sqlalchemy import select

from src.database.connection import session_maker
from src.database.models.users import User
from src.enums.users import Role
from src.schemas.users import UserCreate
from src.services.users import UserService


async def main() -> None:
    async with session_maker() as session:
        existing = await session.execute(select(User).where(User.is_admin.is_(True)))
        if existing.scalar_one_or_none() is not None:
            print("Admin already exists, aborting.")
            return

        service = UserService(session)
        creds = await service.create(
            UserCreate(
                name=os.environ["ADMIN_NAME"],
                surname=os.environ["ADMIN_SURNAME"],
                patronymic=os.environ.get("ADMIN_PATRONYMIC"),
                phone_number=os.environ["ADMIN_PHONE"],
                role=Role.STUDENT,
                is_admin=True,
            )
        )
        await session.commit()

    print("login:", creds.login)
    print("password:", creds.password)


asyncio.run(main())
