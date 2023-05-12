"""
Модуль запросов к API server
"""
import typing

import requests
from aiohttp import ClientSession, ClientResponse, ClientConnectorError

from ..config import base_config
from ..consts import api as ac


async def request(
        method: str,
        url: str,
        headers: dict = None,
        data: dict = None,
        params: dict = None,
        json: dict = None,
        get_content: bool = False
) -> (typing.Optional[ClientResponse], typing.Any):
    """

    :param method: Метод запроса.
    :param url: Адрес запроса.
    :param headers: Заголовки.
    :param data: Данные.
    :param params: Параметры.
    :param json: Данные в формате json.
    :param get_content: Получить content.

    :return: ClientResponse, dict
    """
    async with ClientSession() as session:
        try:
            if params:
                params = {k: v for k, v in params.items() if v is not None}
            async with getattr(session, method)(url, headers=headers, data=data, params=params, json=json) as response:
                if get_content:
                    content = b"" if response.status == 200 else None
                    if content is not None:
                        async for data, _ in response.content.iter_chunks():
                            content += data

                    return response, content
                result = await response.json(content_type=None) if response.status == 200 else None
                return response, result
        except ClientConnectorError:
            pass


def ping_server() -> bool:
    """
    Функция проверки доступности сервера.

    :return: bool
    """
    try:
        res = requests.get(f'{base_config.API_URL}{ac.PING}')
        if res.status_code == 200:
            return True
        print(f'Server {base_config.API_URL} connection not established..')
        return False
    except requests.ConnectionError:
        print(f'Server {base_config.API_URL} connection not established..')
        return False
