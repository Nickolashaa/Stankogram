from functools import lru_cache

from ..services import ConnectionRegistry


@lru_cache
def get_connection_registry() -> ConnectionRegistry:
    return ConnectionRegistry()
