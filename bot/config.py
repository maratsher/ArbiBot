"""
Модуль конфига бота.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    API_URL: str


base_config = Settings(_env_file='.env')
