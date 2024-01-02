from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe que representa as configurações setadas no .env da aplicação.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encode='utf-8')

    DISCORD_TOKEN: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
