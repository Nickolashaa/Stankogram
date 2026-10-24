from collections.abc import Sequence
from datetime import UTC, datetime

import strawberry

from ....enums.events import EventType
from ....services.attachments.schemas import AttachmentResponse
from ....services.attachments.service import AttachmentService
from ....services.chats.participants.schemas import ChatParticipantResponse
from ....services.events.schemas import ChatParticipantEventSchema
from ....services.exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
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


async def _participant_ids(info: AuthorizedAppInfo, chat_id: int) -> list[int]:
    participants = await info.context.services.chat_participant_service.get_list(
        chat_id=chat_id
    )
    return [participant.user_id for participant in participants]


async def _delete_attachment_objects(
    info: AuthorizedAppInfo,
    attachments: Sequence[AttachmentResponse],
) -> None:
    await info.context.services.storage_service.delete(
        AttachmentService.object_keys(attachments)
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
            participant = await info.context.services.chat_participant_service.create(
                chat_id=instance.id,
                user_id=input.participant_id,
            )
            await info.context.session.commit()

            await info.context.services.event_service.publish(
                [participant.user_id],
                ChatParticipantEventSchema(
                    type=EventType.ADD_CHAT_PARTICIPANT,
                    participant=participant,
                ),
            )

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
            participants: list[ChatParticipantResponse] = []
            if input.participant_ids is not None and len(input.participant_ids) > 0:
                for participant_id in input.participant_ids:
                    participants.append(
                        await info.context.services.chat_participant_service.create(
                            chat_id=instance.id,
                            user_id=participant_id,
                        )
                    )
            await info.context.session.commit()

            for participant in participants:
                await info.context.services.event_service.publish(
                    [participant.user_id],
                    ChatParticipantEventSchema(
                        type=EventType.ADD_CHAT_PARTICIPANT,
                        participant=participant,
                    ),
                )

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

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def delete_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
    ) -> Chat | InvalidInputError | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_service.get(chat_id)
            attachments = await info.context.services.attachment_service.get_list(
                chat_id=chat_id
            )
            await info.context.services.chat_service.delete(chat_id)
            await info.context.session.commit()

            await _delete_attachment_objects(info, attachments)

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

            await info.context.services.event_service.publish(
                await _participant_ids(info, instance.chat_id),
                ChatParticipantEventSchema(
                    type=EventType.ADD_CHAT_PARTICIPANT,
                    participant=instance,
                ),
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

        return ChatParticipant.from_schema(instance)

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatAdmin])
    async def remove_participant_from_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
        user_id: int,
    ) -> None:
        instance = await info.context.services.chat_participant_service.get_or_none(
            chat_id=chat_id,
            user_id=user_id,
        )
        recipient_ids = await _participant_ids(info, chat_id)

        await info.context.services.chat_participant_service.delete(
            chat_id=chat_id,
            user_id=user_id,
        )
        await info.context.session.commit()

        if instance is not None:
            await info.context.services.event_service.publish(
                recipient_ids,
                ChatParticipantEventSchema(
                    type=EventType.REMOVE_CHAT_PARTICIPANT,
                    participant=instance,
                ),
            )

    @strawberry.mutation(permission_classes=[IsAuthenticated, IsChatParticipant])
    async def leave_chat(
        self,
        info: AuthorizedAppInfo,
        chat_id: int,
    ) -> Chat | InvalidInputError | ObjectNotFoundError:
        try:
            instance = await info.context.services.chat_service.get(chat_id)
            participant = (
                await info.context.services.chat_participant_service.get_or_none(
                    chat_id=chat_id,
                    user_id=info.context.current_user.id,
                )
            )
            recipient_ids = [
                user_id
                for user_id in await _participant_ids(info, chat_id)
                if user_id != info.context.current_user.id
            ]

            attachments = (
                await info.context.services.attachment_service.get_list(chat_id=chat_id)
                if not recipient_ids
                else []
            )

            await info.context.services.chat_participant_service.leave(
                chat_id=chat_id,
                user_id=info.context.current_user.id,
            )
            await info.context.session.commit()

            await _delete_attachment_objects(info, attachments)

            if participant is not None:
                await info.context.services.event_service.publish(
                    recipient_ids,
                    ChatParticipantEventSchema(
                        type=EventType.REMOVE_CHAT_PARTICIPANT,
                        participant=participant,
                    ),
                )

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
