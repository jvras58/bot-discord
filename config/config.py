from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe que representa as configurações setadas no .env da aplicação.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encode='utf-8')

    DISCORD_TOKEN: str

    AVATAR_SIZE: tuple = (250, 250)
    BACKGROUND_SIZE: tuple = (500, 280)
    BACKGROUND_COLOR: tuple = (56, 56, 56)
    RECTANGLE_COLOR: tuple = (207, 13, 48)
    RECTANGLE_RADIUS: int = 5
    FONT_SIZE: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()
