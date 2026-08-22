from pydantic import BaseModel

from .auth import USER_LOADER


class DataLoaders(BaseModel):
    user_loader: USER_LOADER
