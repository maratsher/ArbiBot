"""
Модуль обработчика команды /start
"""
from aiogram import types

from . import settings
from .. import dp
from ..api import user as user_api
from ..consts import messages as mc, buttons as bc


MODULE_NAME = 'start'


class Steps:
    BUNDLES = 'bundles'
    ARBI_EVENTS = 'arbi_events'
    SETTINGS = 'settings'


async def start_menu(message: types.Message, edit: bool = False):
    """
    Функция отправки стартового меню.

    :param message: Сообщение.
    :param edit: Изменить сообщение.
    """
    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(bc.BUNDLES, callback_data=f'{MODULE_NAME}:{Steps.BUNDLES}'),
        types.InlineKeyboardButton(bc.ARBI_EVENTS, callback_data=f'{MODULE_NAME}:{Steps.ARBI_EVENTS}'),
        types.InlineKeyboardButton(bc.SETTINGS, callback_data=f'{MODULE_NAME}:{Steps.SETTINGS}')
    )

    if edit:
        await message.edit_text(text=mc.START_TEXT, reply_markup=kb, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(text=mc.START_TEXT, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=[MODULE_NAME])
async def start(message: types.Message):
    """
    Функция обработки команды /start
    """
    await user_api.add_user(telegram_id=str(message.chat.id))
    await start_menu(message=message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(MODULE_NAME))
async def callback(callback_query: types.CallbackQuery):
    """
    Функция обработки нажатий на кнопки в стартовом меню
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    if callback_info == Steps.BUNDLES:
        pass
    elif callback_info == Steps.ARBI_EVENTS:
        pass
    elif callback_info == Steps.SETTINGS:
        await settings.settings(message=callback_query.message)
