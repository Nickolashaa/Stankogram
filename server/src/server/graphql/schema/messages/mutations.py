import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage
from ...pubsub import pub_sub
from ...types.errors import ObjectNotFoundError
from ...types.messages import Message, MessageIn


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
            for participant in participants:
                pub_sub.publish(participant.user_id, message)

            return message
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
