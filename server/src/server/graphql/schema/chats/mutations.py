import strawberry

from ....services.exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.chats import IsChatAdmin
from ...types.chats import Chat, ChatIn, ChatParticipant, ChatParticipantIn
from ...types.errors import (
    InvalidInputError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


@strawberry.type
class ChatMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_chat(
        self,
        info: AuthorizedAppInfo,
        input: ChatIn,
        participant_ids: list[int] | None,
    ) -> Chat | InvalidInputError | ObjectNotFoundError | ObjectAlreadyExistsError:
        # Добавить проверку на то, что у этих пользователей уже есть приватный чат
        # Наверное стоит вообще разделить на 2 мутации, а может и не надо
        try:
            instance = await info.context.services.chat_service.create(
                **input.to_service_params()
            )
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)

        await info.context.services.chat_participant_service.create(
            chat_id=instance.id,
            user_id=info.context.current_user.id,
            is_admin=True,
        )

        if participant_ids is not None and len(participant_ids) > 0:
            for participant_id in participant_ids:
                try:
                    await info.context.services.chat_participant_service.create(
                        chat_id=instance.id,
                        user_id=participant_id,
                    )
                except InvalidInput as e:
                    await info.context.session.rollback()
                    return InvalidInputError.from_service_exception(e)
                except ObjectNotFound as e:
                    await info.context.session.rollback()
                    return ObjectNotFoundError.from_service_exception(e)
                except ObjectAlreadyExists as e:
                    await info.context.session.rollback()
                    return ObjectAlreadyExistsError.from_service_exception(e)

        await info.context.session.commit()

        return Chat.from_schema(instance)

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
