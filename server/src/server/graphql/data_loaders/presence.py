from strawberry.dataloader import DataLoader

from ...services.presence import PresenceService

type PRESENCE_LOADER = DataLoader[int, bool]


def build_presence_loader(presence_service: PresenceService) -> PRESENCE_LOADER:
    async def load_fn(keys: list[int]) -> list[bool]:
        return await presence_service.are_online(keys)

    return DataLoader(load_fn=load_fn)
