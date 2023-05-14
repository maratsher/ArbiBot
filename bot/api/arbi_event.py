"""
Модуль запросов к API, связанных с арбитражными ситуациями
"""
from . import _base, schemas
from ..config import base_config
from ..consts import api as ac


async def get_arbi_events() -> list[schemas.ArbiEventInDb] | None:
    """
    Функция получения списка монет

    :return: list[schemas.CoinInDb]
    """
    _, arbi_events = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.ARBI_EVENTS}'
    )
    return [schemas.ArbiEventInDb(**arbi_event) for arbi_event in arbi_events]
