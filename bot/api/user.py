"""
Модуль запросов к API, связанных с пользователем
"""
import typing

from . import _base
from ..config import base_config
from ..consts import api as ac


async def add_user(telegram_id: str):
    """
    Функция привязки telegram к пользователю.

    :param telegram_id: идентификатор telegram
    """
    response, _ = await _base.request(
        method='post',
        url=f'{base_config.API_URL}{ac.USERS_API}/{telegram_id}'
    )
    return response.status == 200


async def delete_telegram(telegram_id: str):
    """
    Функция отвязки telegram от пользователя.

    :param telegram_id: идентификатор telegram
    """
    response, _ = await _base.request(
        method='delete',
        url=f'{base_config.API_URL}{ac.USERS_API}/{telegram_id}',
    )
    return response.status == 200


async def get_user_settings(telegram_id: int) -> typing.Optional[dict]:
    """
    Функция получения настроек пользователя.

    :param telegram_id: идентификатор telegram

    :return: словарь с настройками пользователя
    """
    _, user_settings = await _base.request(
        method='get',
        url=f'{base_config.API_URL}{ac.USERS_API}/{telegram_id}'
    )
    return user_settings


async def update_attendance_settings(
        telegram_id: int,
        attendance_lecture_time: str = None,
        attendance_practice_time: str = None
) -> bool:
    """
    Функция обновления настроек уведомлений журнала посещаемости.

    :param telegram_id: идентификатор telegram
    :param attendance_lecture_time: время уведомлений для лекций
    :param attendance_practice_time: время уведомлений для практик

    :return: успешность изменения настроек
    """
    response, _ = await _base.request(
        method='put',
        url=f'{base_config.API_URL}{ac.USERS_API}/{telegram_id}',
        json={
            'attendance_lecture_time': attendance_lecture_time,
            'attendance_practice_time': attendance_practice_time
        }
    )
    return response.status == 200
