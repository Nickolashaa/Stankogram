import strawberry

from ....services.exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...types.chats import Chat, ChatIn
from ...types.errors import (
    InvalidInputError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)


@strawberry.type
class ChatMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_chat(
        info: AuthorizedAppInfo,
        input: ChatIn,
        participant_ids: list[int] | None,
    ) -> Chat | InvalidInputError | ObjectNotFoundError | ObjectAlreadyExistsError:
        try:
            instance = await info.context.services.chat_service.create(
                **input.to_service_params()
            )
            await info.context.session.commit()
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)

        await info.context.services.chat_participant_service.create(
            chat_id=instance.id,
            user_id=info.context.current_user.id,
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
                    return ObjectAlreadyExistsError.from_service_exception(e)
            await info.context.session.commit()

        return Chat.from_schema(instance)
