"""
Модуль запросов к API, связанных с связками
"""
from . import _base, schemas
from ..config import base_config
from ..consts import api as ac


async def get_bundles(coin_id: int | None = None) -> list[schemas.BundleInDb] | None:
    """
    Функция получения списка монет

    :param coin_id: Идентификатор монеты

    :return: list[schemas.BundleInDb]
    """
    _, bundles = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.BUNDLES}',
        params={'coin_id': coin_id}
    )
    return [schemas.BundleInDb(**bundle) for bundle in bundles]
