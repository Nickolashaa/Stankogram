from cryptography.fernet import Fernet

from ..config import settings


def get_fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY)
