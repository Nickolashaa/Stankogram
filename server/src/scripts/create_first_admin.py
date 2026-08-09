import asyncio

from sqlalchemy import select

from ..database.connection import session_maker
from ..database.models.users import User
from ..enums.users import Role
from ..schemas.users import UserInput
from ..services.users import UserService


async def main() -> None:
    async with session_maker() as session:
        existing = await session.execute(select(User).where(User.is_admin.is_(True)))
        if existing.scalar_one_or_none() is not None:
            print("Admin already exists, aborting.")
            return

        service = UserService(session)
        await service.create(
            UserInput(
                name=input("Name: "),
                surname=input("Surname: "),
                patronymic=input("Patronymic: "),
                email=input("Email: "),
                role=Role.STUDENT,
                is_admin=True,
            )
        )
        await session.commit()

    print("Success, credentials sended in your email.")


asyncio.run(main())
