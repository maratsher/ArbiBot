"""
Модуль обработчика команды /start
"""
from aiogram import types

from . import settings, bundles, bundles_rating, my_arbi_events
from .. import dp
from ..api import user as user_api
from ..consts import messages as mc, buttons as bc


MODULE_NAME = 'start'


class Steps:
    BUNDLE_RATING = 'bundles_rating'
    MY_ARBI_EVENTS = 'my_arbi_events'
    BUNDLES = 'bundles'
    SETTINGS = 'settings'


async def start_menu(message: types.Message, edit: bool = False):
    """
    Функция отправки стартового меню.

    :param message: Сообщение.
    :param edit: Изменить сообщение.
    """
    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(bc.BUNDLE_RATING, callback_data=f'{MODULE_NAME}:{Steps.BUNDLE_RATING}'),
        types.InlineKeyboardButton(bc.MY_ARBI_EVENTS, callback_data=f'{MODULE_NAME}:{Steps.MY_ARBI_EVENTS}'),
        types.InlineKeyboardButton(bc.BUNDLES, callback_data=f'{MODULE_NAME}:{Steps.BUNDLES}'),
        types.InlineKeyboardButton(bc.SETTINGS, callback_data=f'{MODULE_NAME}:{Steps.SETTINGS}')
    )

    if edit:
        await message.edit_text(text=mc.START_TITLE, reply_markup=kb, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(text=mc.START_TITLE, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=[MODULE_NAME])
async def start(message: types.Message):
    """
    Функция обработки команды /start
    """
    success = await user_api.add_user(telegram_id=str(message.chat.id))
    if success:
        await message.answer(text=mc.START_TEXT, parse_mode=types.ParseMode.HTML)
    await start_menu(message=message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(MODULE_NAME))
async def callback(callback_query: types.CallbackQuery):
    """
    Функция обработки нажатий на кнопки в стартовом меню
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    if callback_info == Steps.BUNDLE_RATING:
        await bundles_rating.bundles_rating_menu(message=callback_query.message)
    elif callback_info == Steps.MY_ARBI_EVENTS:
        await my_arbi_events.my_arbi_events_menu(message=callback_query.message)
    elif callback_info == Steps.BUNDLES:
        await bundles.bundles_menu(message=callback_query.message)
    elif callback_info == Steps.SETTINGS:
        await settings.settings_menu(message=callback_query.message)
