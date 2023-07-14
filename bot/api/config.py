"""
Модуль конфигураций.
"""
from pydantic import BaseSettings


class Database(BaseSettings):
    """
    Класс констант для данных.
    """
    MAX_LEN_ID: int = 2147483647

    MAX_VOLUME: float = 100000
    MAX_THRESHOLD: float = 100
    MAX_EPSILON: float = 1
    MAX_DIFFERENCE: float = 100

    class Config:
        case_sensitive = True


db_config = Database()
