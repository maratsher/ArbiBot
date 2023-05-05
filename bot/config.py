"""
Модуль конфига бота.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    API_URL: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str


base_config = Settings(_env_file='.env')
