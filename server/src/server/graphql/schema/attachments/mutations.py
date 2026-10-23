import strawberry

from ....services.attachments.service import THUMBNAIL_CONTENT_TYPE
from ....services.exceptions import InvalidInput, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.messages import CanCreateMessage
from ...types.attachments import Attachment, AttachmentUpload, AttachmentUploadIn
from ...types.errors import InvalidInputError, ObjectNotFoundError


@strawberry.type
class AttachmentMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated, CanCreateMessage])
    async def create_attachment_upload(
        self,
        info: AuthorizedAppInfo,
        input: AttachmentUploadIn,
    ) -> AttachmentUpload | InvalidInputError | ObjectNotFoundError:
        try:
            instance = await info.context.services.attachment_service.create(
                **input.to_create_service_params(info.context.current_user.id)
            )
            await info.context.session.commit()
        except InvalidInput as e:
            await info.context.session.rollback()
            return InvalidInputError.from_service_exception(e)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

        storage = info.context.services.storage_service

        return AttachmentUpload(
            attachment=Attachment.from_schema(instance),
            upload_url=storage.upload_url(instance.key, instance.content_type),
            thumbnail_upload_url=(
                storage.upload_url(instance.thumbnail_key, THUMBNAIL_CONTENT_TYPE)
                if instance.thumbnail_key is not None
                else None
            ),
        )
