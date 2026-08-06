import asyncio

from sqlalchemy import select

from ..database.connection import session_maker
from ..database.models.users import User
from ..enums.users import Role
from ..schemas.users import UserCreate
from ..services.users import UserService


async def main() -> None:
    async with session_maker() as session:
        existing = await session.execute(select(User).where(User.is_admin.is_(True)))
        if existing.scalar_one_or_none() is not None:
            print("Admin already exists, aborting.")
            return

        service = UserService(session)
        creds = await service.create(
            UserCreate(
                name=input("Name: "),
                surname=input("Surname: "),
                patronymic=input("Patronymic: "),
                phone_number=input("Phone number: "),
                role=Role.STUDENT,
                is_admin=True,
            )
        )
        await session.commit()

    print("login:", creds.login)
    print("password:", creds.password)


asyncio.run(main())
