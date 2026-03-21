from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    uvicorn_host: str
    uvicorn_port: int


config = Settings()  # type: ignore[call-arg]
