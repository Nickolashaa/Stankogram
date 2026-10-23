from ..services.storage import StorageService


def get_storage_service() -> StorageService:
    return StorageService()
