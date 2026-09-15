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


async def _sync_mentions(
    info: AuthorizedAppInfo,
    message_id: int,
    chat_id: int,
    mentioned_user_ids: list[int],
) -> None:
    participants = await info.context.services.chat_participant_service.get_list(
        chat_id=chat_id
    )
    participant_ids = {participant.user_id for participant in participants}

    await info.context.services.notification_service.sync_for_message(
        message_id=message_id,
        user_ids=[
            user_id
            for user_id in dict.fromkeys(mentioned_user_ids)
            if user_id in participant_ids and user_id != info.context.current_user.id
        ],
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
            await _sync_mentions(
                info=info,
                message_id=instance.id,
                chat_id=instance.chat_id,
                mentioned_user_ids=input.mentioned_user_ids,
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
            await _sync_mentions(
                info=info,
                message_id=instance.id,
                chat_id=instance.chat_id,
                mentioned_user_ids=input.mentioned_user_ids,
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
