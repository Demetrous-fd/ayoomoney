from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")
    yoomoney_notification_secret: str = Field(...)
    redis_dsn: str = Field(default="redis://localhost:6379")


settings = Settings()
