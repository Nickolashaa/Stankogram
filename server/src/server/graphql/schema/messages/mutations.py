import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage
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
                type=input.type,
                text=input.text,
            )
            await info.context.session.commit()
            return Message.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
