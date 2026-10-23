from strawberry.dataloader import DataLoader

from ...services.attachments import AttachmentService
from ..types.attachments import Attachment

type ATTACHMENTS_BY_MESSAGE_ID_LOADER = DataLoader[int, list[Attachment]]


def build_attachments_by_message_id_loader(
    attachment_service: AttachmentService,
) -> ATTACHMENTS_BY_MESSAGE_ID_LOADER:
    async def load_fn(keys: list[int]) -> list[list[Attachment]]:
        message_id_to_attachments: dict[int, list[Attachment]] = {}

        instances = await attachment_service.get_list(message_ids=keys)

        for instance in instances:
            if instance.message_id is None:
                continue
            message_id_to_attachments.setdefault(instance.message_id, []).append(
                Attachment.from_schema(instance)
            )

        return [message_id_to_attachments.get(key, []) for key in keys]

    return DataLoader(load_fn=load_fn)
