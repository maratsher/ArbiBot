"""
Модуль запросов к API, связанных с монетами
"""
from . import _base, schemas
from ..config import base_config
from ..consts import api as ac


async def get_coins() -> list[schemas.CoinInDb] | None:
    """
    Функция получения списка монет
    """
    _, coins = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.COINS}'
    )
    return [schemas.CoinInDb(**coin) for coin in coins]
