import asyncio
from collections.abc import Sequence

import strawberry

from ....config import settings
from ....enums.events import EventType
from ....services.attachments.schemas import AttachmentResponse
from ....services.attachments.service import AttachmentService
from ....services.events.schemas import MessageEventSchema
from ....services.exceptions import InvalidInput, ObjectNotFound
from ....services.storage import StorageService
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage, CanDeleteMessage, IsMessageAuthor
from ...types.errors import InvalidInputError, ObjectNotFoundError
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


async def _attachments_to_attach(
    info: AuthorizedAppInfo,
    chat_id: int,
    attachment_ids: Sequence[int],
) -> list[AttachmentResponse]:
    ids = list(dict.fromkeys(attachment_ids))
    if not ids:
        return []

    if len(ids) > settings.ATTACHMENTS_MAX_PER_MESSAGE:
        raise InvalidInput(
            f"Message cannot have more than "
            f"{settings.ATTACHMENTS_MAX_PER_MESSAGE} attachments"
        )

    instances = await info.context.services.attachment_service.get_list(
        ids=ids,
        chat_id=chat_id,
        user_id=info.context.current_user.id,
        is_attached=False,
    )
    if len(instances) != len(ids):
        raise ObjectNotFound("Some of the attachments do not exist")

    return instances


async def _uploaded_size(
    storage: StorageService,
    instance: AttachmentResponse,
) -> tuple[int | None, int | None]:
    if instance.thumbnail_key is None:
        return await storage.get_size(instance.key), 0

    return await asyncio.gather(
        storage.get_size(instance.key),
        storage.get_size(instance.thumbnail_key),
    )


async def _uploaded_sizes(
    info: AuthorizedAppInfo,
    instances: Sequence[AttachmentResponse],
) -> dict[int, int]:
    storage = info.context.services.storage_service

    sizes = await asyncio.gather(
        *[_uploaded_size(storage, instance) for instance in instances]
    )

    uploaded: dict[int, int] = {}
    for instance, (size, thumbnail_size) in zip(instances, sizes, strict=True):
        if size is None or thumbnail_size is None:
            raise InvalidInput(f"Attachment {instance.id} is not uploaded")

        if size > AttachmentService.get_max_size(instance.kind):
            raise InvalidInput(f"Attachment {instance.id} is too large")

        if thumbnail_size > settings.ATTACHMENT_THUMBNAIL_MAX_SIZE:
            raise InvalidInput(f"Attachment {instance.id} thumbnail is too large")

        uploaded[instance.id] = size

    return uploaded


@strawberry.type
class MessageMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated, CanCreateMessage])
    async def create_message(
        self,
        info: AuthorizedAppInfo,
        input: MessageIn,
    ) -> Message | InvalidInputError | ObjectNotFoundError:
        try:
            attachments = await _attachments_to_attach(
                info=info,
                chat_id=input.chat_id,
                attachment_ids=input.attachment_ids,
            )
            sizes = await _uploaded_sizes(info, attachments)

            if input.text.strip() == "" and not attachments:
                raise InvalidInput("Message cannot be empty")

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
            await info.context.services.attachment_service.attach(
                ids=[attachment.id for attachment in attachments],
                message_id=instance.id,
                sizes=sizes,
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
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
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
            attachments = await info.context.services.attachment_service.get_list(
                message_id=message_id
            )
            await info.context.services.message_service.delete(message_id)
            await info.context.session.commit()

            await info.context.services.storage_service.delete(
                AttachmentService.object_keys(attachments)
            )

            await info.context.services.event_service.publish(
                await _participant_ids(info, instance.chat_id),
                MessageEventSchema(type=EventType.DELETE_MESSAGE, message=instance),
            )

            return Message.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
