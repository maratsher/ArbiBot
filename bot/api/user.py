"""
Модуль запросов к API, связанных с пользователем
"""
from . import _base, schemas
from ..config import base_config
from ..consts import api as ac


async def add_user(telegram_id: str):
    """
    Функция привязки telegram к пользователю.

    :param telegram_id: идентификатор telegram
    """
    response, _ = await _base.request(
        method='post',
        url=f'{base_config.API_URL}{ac.USERS}',
        json={'telegram_id': telegram_id}
    )
    return response.status == 200


async def add_user_bundle(telegram_id: str, data: schemas.UserBundleAdd):
    """
    Функция привязки telegram к пользователю.

    :param telegram_id: идентификатор telegram
    :param data: схема
    """
    response, _ = await _base.request(
        method='post',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}/bundle',
        json=data.dict()
    )
    return response.status == 200


async def get_user(telegram_id: str) -> schemas.UserInDb | None:
    """
    Функция получения пользователя.

    :param telegram_id: идентификатор telegram

    :return: schemas.UserInDb
    """
    _, user = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}'
    )
    if user:
        return schemas.UserInDb(**user)


async def get_user_bundles(telegram_id: str) -> list[schemas.BundleInDb] | None:
    """
    Функция получения списка связок пользователя

    :param telegram_id: идентификатор telegram

    :return: list[schemas.BundleInDb]
    """
    _, bundles = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}/bundles'
    )
    return [schemas.BundleInDb(**bundle) for bundle in bundles]


async def get_arbi_events(telegram_id: str) -> list[schemas.ArbiEventInDb] | None:
    """
    Функция получения списка арбитражных ситуаций

    :param telegram_id: идентификатор telegram

    :return: list[schemas.ArbiEventInDb]
    """
    _, arbi_events = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}/arbi_events'
    )
    return [schemas.ArbiEventInDb(**arbi_event) for arbi_event in arbi_events]



async def update_base_coin(data: schemas.UserBaseCoinUpdate):
    """
    Функция обновления расчетной монеты пользователя.

    :param data: схема
    """
    response, _ = await _base.request(
        method='put',
        url=f'{base_config.API_URL}{ac.USERS}/base_coin_id',
        json=data.dict()
    )
    return response.status == 200


async def update_volume(data: schemas.UserVolumeUpdate):
    """
    Функция обновления объема торгов пользователя.

    :param data: схема
    """
    response, _ = await _base.request(
        method='put',
        url=f'{base_config.API_URL}{ac.USERS}/volume',
        json=data.dict()
    )
    return response.status == 200


async def update_threshold(data: schemas.UserThresholdUpdate):
    """
    Функция обновления порога арбитражной ситуации пользователя.

    :param data: схема
    """
    response, _ = await _base.request(
        method='put',
        url=f'{base_config.API_URL}{ac.USERS}/threshold',
        json=data.dict()
    )
    return response.status == 200


async def delete_user(telegram_id: str):
    """
    Функция отвязки telegram от пользователя.

    :param telegram_id: идентификатор telegram
    """
    response, _ = await _base.request(
        method='delete',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}',
    )
    return response.status == 200


async def delete_user_bundle(telegram_id: str, bundle_id: int):
    """
    Функция отвязки telegram от пользователя.

    :param telegram_id: идентификатор telegram
    :param bundle_id: идентификатор связки
    """
    response, _ = await _base.request(
        method='delete',
        url=f'{base_config.API_URL}{ac.USERS}/{telegram_id}/bundle',
        params={'bundle_id': bundle_id}
    )
    return response.status == 200
