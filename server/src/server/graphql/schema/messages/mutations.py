from collections.abc import Sequence

import strawberry

from ....enums.events import EventType
from ....services.events.schemas import MessageEventSchema
from ....services.exceptions import ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage, CanDeleteMessage, IsMessageAuthor
from ...types.errors import ObjectNotFoundError
from ...types.messages import Message, MessageIn, MessageUpdateIn


async def _participant_ids(info: AuthorizedAppInfo, chat_id: int) -> list[int]:
    participants = await info.context.services.chat_participant_service.get_list(
        chat_id=chat_id
    )
    return [participant.user_id for participant in participants]


async def _sync_mentions(
    info: AuthorizedAppInfo,
    message_id: int,
    participant_ids: Sequence[int],
    mentioned_user_ids: list[int],
) -> None:
    allowed_ids = set(participant_ids)

    await info.context.services.notification_service.sync_for_message(
        message_id=message_id,
        user_ids=[
            user_id
            for user_id in dict.fromkeys(mentioned_user_ids)
            if user_id in allowed_ids and user_id != info.context.current_user.id
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
            if input.reply_to_message_id is not None:
                reply_to = await info.context.services.message_service.get_or_none(
                    input.reply_to_message_id
                )
                if reply_to is None or reply_to.chat_id != input.chat_id:
                    return ObjectNotFoundError(
                        message=(
                            f"Message with id {input.reply_to_message_id} not found"
                        )
                    )

            instance = await info.context.services.message_service.create(
                user_id=info.context.current_user.id,
                chat_id=input.chat_id,
                text=input.text,
                reply_to_message_id=input.reply_to_message_id,
            )
            participant_ids = await _participant_ids(info, instance.chat_id)
            await _sync_mentions(
                info=info,
                message_id=instance.id,
                participant_ids=participant_ids,
                mentioned_user_ids=input.mentioned_user_ids,
            )
            await info.context.session.commit()

            await info.context.services.event_service.publish(
                participant_ids,
                MessageEventSchema(type=EventType.CREATE_MESSAGE, message=instance),
            )

            return Message.from_schema(instance)
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
            participant_ids = await _participant_ids(info, instance.chat_id)
            await _sync_mentions(
                info=info,
                message_id=instance.id,
                participant_ids=participant_ids,
                mentioned_user_ids=input.mentioned_user_ids,
            )
            await info.context.session.commit()

            await info.context.services.event_service.publish(
                participant_ids,
                MessageEventSchema(type=EventType.UPDATE_MESSAGE, message=instance),
            )

            return Message.from_schema(instance)
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

            await info.context.services.event_service.publish(
                await _participant_ids(info, instance.chat_id),
                MessageEventSchema(type=EventType.DELETE_MESSAGE, message=instance),
            )

            return Message.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
