"""
Обертка класса Bot с обработкой ошибок и логирование.
"""
import typing
import inspect

from aiogram import Bot, types
import aiogram.utils.exceptions as exceptions

import bot


class BotWrapper(Bot):
    """
    Класс для обработки ошибок бота и логирования.
    """

    def __init__(self, token):
        super().__init__(token)

    async def send_message(self, chat_id: typing.Union[int, str], text: str, *args, **kwargs):
        """
        Метод отправки текстового сообщения.

        :param chat_id: идентификатор чата пользователя.
        :param text: текст сообщения.
        :param args: любые аргументы.
        :param kwargs: любые аргументы.
        """
        result, error = None, None

        try:
            result = await super().send_message(chat_id, text, *args, **kwargs)
        except Exception:
            pass

        return result
