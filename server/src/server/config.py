from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str = Field(min_length=1)
    POSTGRES_USER: str = Field(min_length=1)
    POSTGRES_PASSWORD: str = Field(min_length=1)

    LIMIT: int = 10
    OFFSET: int = 0

    PASSWORD_LEN: int = 8
    PASSWORD_RESET_CODE_LEN: int = 6
    PASSWORD_RESET_CODE_EXP_MINUTES: int = 10

    APP_BASE_URL: str = "https://stankogram.ru"

    UVICORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 8000

    JWT_SECRET_KEY: str = Field(min_length=32)
    JWT_ENCRYPTION_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXP_MINUTES: int = 5
    JWT_REFRESH_EXP_DAYS: int = 14

    REFRESH_TOKEN_COOKIE_PATH: str = "/api"

    SMTP_LOGIN: str = Field(min_length=1)
    SMTP_PASSWORD: str = Field(min_length=1)
    SMTP_SERVER: str = "smtp.yandex.ru"
    SMTP_PORT: int = 587

    ENCRYPTION_KEY: str = Field(min_length=44)

    USERS_IMPORT_MAX_ROWS: int = 100
    USERS_IMPORT_MAX_SCAN_ROWS: int = 10000
    USERS_IMPORT_MAX_FILE_SIZE: int = 5 * 1024 * 1024
    USERS_IMPORT_MAX_VALUE_LEN: int = 100

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@database:5432/{self.POSTGRES_DB}"
        )


settings = Settings()
