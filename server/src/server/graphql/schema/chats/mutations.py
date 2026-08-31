from datetime import UTC, datetime

import strawberry

from ....services.exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.chats import IsChatAdmin, IsChatParticipant
from ...types.chats import (
    Chat,
    ChatParticipant,
    ChatParticipantIn,
    ChatUpdateIn,
    PrivateChatIn,
    PublicChatIn,
)
from ...types.errors import (
    InvalidInputError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


@strawberry.type
class ChatMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_private_chat(
        self,
        info: AuthorizedAppInfo,
        input: PrivateChatIn,
    ) -> Chat | InvalidInputError | ObjectNotFoundError | ObjectAlreadyExistsError:
        try:
            already_exists = await info.context.services.chat_participant_service.is_private_chat_exists(  # noqa: E501
                first_user_id=info.context.current_user.id,
                second_user_id=input.participant_id,
            )
            if already_exists:
                raise ObjectAlreadyExists("Private chat with this user already exists")

            instance = await info.context.services.chat_service.create(
                **input.to_service_params()
            )
            await info.context.services.chat_participant_service.create(
                chat_id=instance.id,
                user_id=info.context.current_user.id,
            )
            await info.context.services.chat_participant_service.create(
                chat_id=instance.id,
                user_id=input.participant_id,
            )
            await info.context.session.commit()
            return Chat.from_schema(instance)
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_public_chat(
        self,
        info: AuthorizedAppInfo,
        input: PublicChatIn,
    ) -> Chat | InvalidInputError | ObjectNotFoundError | ObjectAlreadyExistsError:
        try:
            instance = await info.context.services.chat_service.create(
                **input.to_service_params()
            )
            await info.context.services.chat_participant_service.create(
                chat_id=instance.id,
                user_id=info.context.current_user.id,
                is_admin=True,
            )
            if input.participant_ids is not None and len(input.participant_ids) > 0:
                for participant_id in input.participant_ids:
                    await info.context.services.chat_participant_service.create(
                        chat_id=instance.id,
                        user_id=participant_id,
                    )
            await info.context.session.commit()
            return Chat.from_schema(instance)
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatAdmin])
    async def update_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
        input: ChatUpdateIn,
    ) -> Chat | InvalidInputError | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_service.update(
                id=chat_id, **input.to_service_params()
            )
            await info.context.session.commit()
            return Chat.from_schema(instance)
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatAdmin])
    async def add_participant_to_chat(
        self,
        info: AuthorizedAppInfo,
        input: ChatParticipantIn,
    ) -> (
        ChatParticipant
        | ObjectNotFoundError
        | ObjectAlreadyExistsError
        | InvalidInputError
    ):
        try:
            instance = await info.context.services.chat_participant_service.create(
                **input.to_create_service_params(),
            )
            await info.context.session.commit()
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
        except ObjectAlreadyExists as e:
            await info.context.session.rollback()
            return ObjectAlreadyExistsError.from_service_exception(e)

        return ChatParticipant.from_schema(instance)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatAdmin])
    async def remove_participant_from_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
        user_id: int,
    ) -> None:
        await info.context.services.chat_participant_service.delete(
            chat_id=chat_id,
            user_id=user_id,
        )
        await info.context.session.commit()

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatParticipant])
    async def leave_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
    ) -> Chat | InvalidInputError | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_service.get(chat_id)
            await info.context.services.chat_participant_service.leave(
                chat_id=chat_id,
                user_id=info.context.current_user.id,
            )
            await info.context.session.commit()
            return Chat.from_schema(instance)
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatAdmin])
    async def update_chat_participant_permissions(
        self,
        info: AuthorizedAppInfo,
        input: ChatParticipantIn,
    ) -> ChatParticipant | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_participant_service.update(
                **input.to_create_service_params()
            )
            await info.context.session.commit()
            return ChatParticipant.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatParticipant])
    async def mark_chat_read(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
    ) -> ChatParticipant | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_participant_service.update(
                chat_id=chat_id,
                user_id=info.context.current_user.id,
                last_read_at=datetime.now(UTC),
            )
            await info.context.session.commit()
            return ChatParticipant.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
