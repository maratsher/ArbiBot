"""
Модуль обработчика команды /unlink
"""
from aiogram import types

from .. import dp
from ..api import user as user_api
from ..consts import messages as mc


MODULE_NAME = 'unlink'


@dp.message_handler(commands=[MODULE_NAME])
async def unlink(message: types.Message):
    """
    Функция обработки команды /unlink
    """
    success = await user_api.delete_user(telegram_id=str(message.chat.id))
    await message.answer(text=mc.UNLINK_SUCCESS if success else mc.ALREADY_UNLINKED, parse_mode=types.ParseMode.HTML)
