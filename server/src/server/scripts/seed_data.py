import asyncio
import json
from pathlib import Path

import bcrypt
from cryptography.fernet import Fernet

from ..config import ENCRYPTION_KEY
from ..database.connection import session_maker
from ..database.models.auth import User
from ..database.models.chats import Chat, ChatParticipant
from ..database.models.messages import Message
from ..enums.chats import ChatType
from ..enums.messages import MessageType
from ..enums.users import UserRole

_TEST_DATA_PATH = Path(__file__).parent / "test_data.json"
_TEST_DATA = json.loads(_TEST_DATA_PATH.read_text(encoding="utf-8"))

_SEED_PASSWORD: str = _TEST_DATA["seed_password"]

_USERS_DATA: list[dict] = [
    {**user, "role": UserRole(user["role"])} for user in _TEST_DATA["users"]
]

_CHATS_DATA: list[dict] = [
    {**chat, "type": ChatType(chat["type"])} for chat in _TEST_DATA["chats"]
]

_CHAT_PARTICIPANTS_INDEXES: list[tuple[int, int, bool]] = [
    tuple(entry) for entry in _TEST_DATA["chat_participants_indexes"]
]

_MESSAGES_INDEXES: list[tuple[int, int, str]] = [
    tuple(entry) for entry in _TEST_DATA["messages_indexes"]
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
        ChatParticipant(
            chat_id=chats[chat_idx].id,
            user_id=users[user_idx].id,
            is_admin=is_admin,
        )
        for chat_idx, user_idx, is_admin in _CHAT_PARTICIPANTS_INDEXES
    ]
    session.add_all(participants)
    await session.flush()

    return participants


async def _seed_messages(
    session, chats: list[Chat], users: list[User]
) -> list[Message]:
    fernet = Fernet(ENCRYPTION_KEY)

    messages = [
        Message(
            chat_id=chats[chat_idx].id,
            user_id=users[user_idx].id,
            encrypted_text=fernet.encrypt(text.encode()).decode(),
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

    print("Success!")


def main() -> None:
    asyncio.run(_seed())
