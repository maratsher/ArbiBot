"""
Модуль запросов к API, связанных с биржами
"""
from . import _base, schemas
from ..config import base_config
from ..consts import api as ac


async def get_exchange(exchange_id: int) -> schemas.ExchangeInDb | None:
    """
    Функция получения биржи

    :return: list[schemas.ExchangeInDb]
    """
    _, exchange = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.EXCHANGES}/{exchange_id}'
    )
    return schemas.ExchangeInDb(**exchange)


async def get_exchanges() -> list[schemas.ExchangeInDb] | None:
    """
    Функция получения списка бирж

    :return: list[schemas.ExchangeInDb]
    """
    _, exchanges = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.EXCHANGES}'
    )
    return [schemas.ExchangeInDb(**exchange) for exchange in exchanges]
