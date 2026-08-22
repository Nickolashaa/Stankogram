import asyncio

import bcrypt

from ..database.connection import session_maker
from ..database.models.auth import User
from ..database.models.chats import Chat, ChatParticipant
from ..database.models.messages import Message
from ..enums.chats import ChatType
from ..enums.messages import MessageType
from ..enums.users import UserRole

_SEED_PASSWORD = "password123"

_USERS_DATA: list[dict] = [
    {
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "email": "ivanov@stankogram.ru",
        "role": UserRole.TEACHER,
        "is_admin": True,
    },
    {
        "name": "Мария",
        "surname": "Петрова",
        "patronymic": "Сергеевна",
        "email": "petrova@stankogram.ru",
        "role": UserRole.TEACHER,
        "is_admin": False,
    },
    {
        "name": "Алексей",
        "surname": "Сидоров",
        "patronymic": "Дмитриевич",
        "email": "sidorov@stankogram.ru",
        "role": UserRole.STUDENT,
        "is_admin": False,
    },
    {
        "name": "Ольга",
        "surname": "Кузнецова",
        "patronymic": "Викторовна",
        "email": "kuznecova@stankogram.ru",
        "role": UserRole.STUDENT,
        "is_admin": False,
    },
    {
        "name": "Дмитрий",
        "surname": "Смирнов",
        "patronymic": "Андреевич",
        "email": "smirnov@stankogram.ru",
        "role": UserRole.STUDENT,
        "is_admin": False,
    },
    {
        "name": "Екатерина",
        "surname": "Новикова",
        "patronymic": "Павловна",
        "email": "novikova@stankogram.ru",
        "role": UserRole.STUDENT,
        "is_admin": False,
    },
]

_CHATS_DATA: list[dict] = [
    {"type": ChatType.PRIVATE, "title": None},
    {"type": ChatType.PUBLIC, "title": "Группа ЧПУ-21"},
    {"type": ChatType.PUBLIC, "title": "Общий чат кафедры"},
]

_CHAT_PARTICIPANTS_INDEXES: list[tuple[int, int]] = [
    (0, 0),
    (0, 2),
    (1, 0),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
]

_MESSAGES_INDEXES: list[tuple[int, int, str]] = [
    (
        0,
        2,
        "Здравствуйте, Иван Иванович! Подскажите, пожалуйста, по лабораторной работе.",
    ),
    (0, 0, "Добрый день, Алексей! Слушаю вас."),
    (0, 2, "Не могу разобраться с настройкой станка ЧПУ, можно после пар подойти?"),
    (0, 0, "Да, конечно, жду вас в 15:00."),
    (1, 0, "Добрый день! Напоминаю про сдачу отчёта до пятницы."),
    (1, 3, "Здравствуйте! А в каком формате сдавать?"),
    (1, 4, "Присоединяюсь к вопросу."),
    (1, 0, "В формате PDF, как обычно."),
    (2, 1, "Коллеги, завтра собрание кафедры в 10:00."),
    (2, 5, "Спасибо за информацию!"),
    (2, 2, "Будет ли онлайн-трансляция?"),
    (2, 1, "Да, ссылку отправлю позже."),
]


async def _seed_users(session) -> list[User]:
    hashed_password = bcrypt.hashpw(
        password=_SEED_PASSWORD.encode(), salt=bcrypt.gensalt()
    ).decode()

    users = [User(hashed_password=hashed_password, **data) for data in _USERS_DATA]
    session.add_all(users)
    await session.flush()

    return users


async def _seed_chats(session) -> list[Chat]:
    chats = [Chat(**data) for data in _CHATS_DATA]
    session.add_all(chats)
    await session.flush()

    return chats


async def _seed_chat_participants(
    session, chats: list[Chat], users: list[User]
) -> list[ChatParticipant]:
    participants = [
        ChatParticipant(chat_id=chats[chat_idx].id, user_id=users[user_idx].id)
        for chat_idx, user_idx in _CHAT_PARTICIPANTS_INDEXES
    ]
    session.add_all(participants)
    await session.flush()

    return participants


async def _seed_messages(
    session, chats: list[Chat], users: list[User]
) -> list[Message]:
    messages = [
        Message(
            chat_id=chats[chat_idx].id,
            user_id=users[user_idx].id,
            encrypted_text=text,
            type=MessageType.TEXT,
        )
        for chat_idx, user_idx, text in _MESSAGES_INDEXES
    ]
    session.add_all(messages)
    await session.flush()

    return messages


async def _seed() -> None:
    async with session_maker() as session:
        users = await _seed_users(session)
        chats = await _seed_chats(session)
        await _seed_chat_participants(session, chats, users)
        await _seed_messages(session, chats, users)

        await session.commit()

    print(f"Seeded {len(users)} users, {len(chats)} chats and their messages.")
    print(f'All seeded users have password "{_SEED_PASSWORD}".')


def main() -> None:
    asyncio.run(_seed())
