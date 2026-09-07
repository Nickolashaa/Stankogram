import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage, CanDeleteMessage, IsMessageAuthor
from ...pubsub import pub_sub
from ...types.errors import ObjectNotFoundError
from ...types.messages import (
    CreateMessage,
    DeleteMessage,
    Message,
    MessageIn,
    MessageUpdateIn,
    UpdateMessage,
)


@strawberry.type
class MessageMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated, CanCreateMessage])
    async def create_message(
        self,
        info: AuthorizedAppInfo,
        input: MessageIn,
    ) -> Message | ObjectNotFoundError:
        try:
            instance = await info.context.services.message_service.create(
                user_id=info.context.current_user.id,
                chat_id=input.chat_id,
                text=input.text,
            )
            await info.context.session.commit()

            message = Message.from_schema(instance)
            participants = (
                await info.context.services.chat_participant_service.get_list(
                    chat_id=input.chat_id
                )
            )
            event = CreateMessage(message=message)
            for participant in participants:
                pub_sub.publish(participant.user_id, event)

            return message
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsMessageAuthor])
    async def update_message(
        self,
        info: AuthorizedAppInfo,
        message_id: int,
        input: MessageUpdateIn,
    ) -> Message | ObjectNotFoundError:
        try:
            instance = await info.context.services.message_service.update(
                id=message_id,
                text=input.text,
            )
            await info.context.session.commit()

            message = Message.from_schema(instance)
            participants = (
                await info.context.services.chat_participant_service.get_list(
                    chat_id=message.chat_id
                )
            )
            event = UpdateMessage(message=message)
            for participant in participants:
                pub_sub.publish(participant.user_id, event)

            return message
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated, CanDeleteMessage])
    async def delete_message(
        self,
        info: AuthorizedAppInfo,
        message_id: int,
    ) -> Message | ObjectNotFoundError:
        try:
            instance = await info.context.services.message_service.get(message_id)
            await info.context.services.message_service.delete(message_id)
            await info.context.session.commit()

            message = Message.from_schema(instance)
            participants = (
                await info.context.services.chat_participant_service.get_list(
                    chat_id=message.chat_id
                )
            )
            event = DeleteMessage(message=message)
            for participant in participants:
                pub_sub.publish(participant.user_id, event)

            return message
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
