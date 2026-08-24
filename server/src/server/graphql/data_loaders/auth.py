from strawberry.dataloader import DataLoader

from ...services.auth import AuthService
from ..types.auth import User

type USER_LOADER = DataLoader[int, User]


def build_users_loader(auth_service: AuthService) -> USER_LOADER:
    async def load_users(keys: list[int]) -> list[User]:
        user_id_to_user = {
            user.id: user for user in await auth_service.get_list(ids=keys)
        }

        return [
            User.from_schema(instance)
            for instance in [user_id_to_user[key] for key in keys]
        ]

    return DataLoader(load_fn=load_users)
