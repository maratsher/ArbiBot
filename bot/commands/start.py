"""
Модуль обработчика команды /start
"""
from aiogram import types

from .. import dp
from ..api import user as user_api
from ..consts import messages as mc


MODULE_NAME = 'start'


@dp.message_handler(commands=[MODULE_NAME])
async def start(message: types.Message):
    """
    Функция обработки команды /start
    """
    await user_api.add_user(telegram_id=str(message.chat.id))
    await message.answer(text=mc.START_TEXT, parse_mode=types.ParseMode.HTML)
