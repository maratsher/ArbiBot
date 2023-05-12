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
