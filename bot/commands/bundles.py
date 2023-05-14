"""
Модуль связок
"""
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from . import start
from .. import dp
from ..consts import (
    messages as mc,
    buttons as bc
)
from ..api import (
    user as user_api,
    coin as coin_api,
    bundle as bundle_api,
    schemas
)


MODULE_NAME = 'bundles'


class Steps:
    ADD_BUNDLE = 'add_bundle'
    DELETE_BUNDLE = 'delete_bundle'
    BACK = 'back'


class StorageDataFields:
    LAST_MESSAGE = 'last_bot_message'


class SettingsForm(StatesGroup):
    get_volume = State()
    get_threshold = State()


async def bundles_menu(message: types.Message):
    """
    Функция обработки меню связок
    """
    user_bundles = await user_api.get_user_bundles(telegram_id=str(message.chat.id))

    kb = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton(bc.ADD_BUNDLE, callback_data=f'{MODULE_NAME}:{Steps.ADD_BUNDLE}')
    )

    text = f"{mc.BUNDLES_TITLE}{mc.LINE}"

    if user_bundles:
        kb.insert(types.InlineKeyboardButton(bc.DELETE_BUNDLE, callback_data=f'{MODULE_NAME}:{Steps.DELETE_BUNDLE}'))
        for num, bundle in enumerate(user_bundles):
            text += f"<b>{num + 1}.</b> {bundle.coin.ticker} - {bundle.exchange1.name} 🔄 {bundle.exchange2.name}\n"
    else:
        text += mc.BUNDLES_EMPTY

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}'))

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


async def chose_bundle_coin(message: types.Message):
    """
    Функция обработки меню выбора монеты для связки
    """
    coins = await coin_api.get_coins()

    kb = types.InlineKeyboardMarkup(row_width=3)\

    for coin in coins:
        kb.insert(types.InlineKeyboardButton(
            coin.ticker, callback_data=f'{MODULE_NAME}:{Steps.ADD_BUNDLE}:{coin.id}'
        ))

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{Steps.ADD_BUNDLE}'))

    text = f"{mc.BUNDLES_TITLE}{mc.LINE}{mc.BUNDLES_COIN}"

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


async def chose_bundle(message: types.Message, coin_id: int):
    """
    Функция обработки меню выбора связки
    """
    bundles = await bundle_api.get_bundles(coin_id=coin_id)

    kb = types.InlineKeyboardMarkup(row_width=2)

    coin_ticker = None

    for bundle in bundles:
        if coin_ticker is None:
            coin_ticker = bundle.coin.ticker
        kb.insert(types.InlineKeyboardButton(
            f"{bundle.exchange1.name} 🔄 {bundle.exchange2.name}",
            callback_data=f'{MODULE_NAME}:{Steps.ADD_BUNDLE}:{coin_id}:{bundle.id}'
        ))

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.ADD_BUNDLE}'))

    text = f"{mc.BUNDLES_TITLE}{mc.LINE}{mc.BUNDLES_EXCHANGE.format(coin_ticker)}"

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


async def chose_delete_bundle(message: types.Message, telegram_id: str):
    """
    Функция обработки меню выбора связки для удаления
    """
    bundles = await user_api.get_user_bundles(telegram_id=telegram_id)

    kb = types.InlineKeyboardMarkup(row_width=1)

    for bundle in bundles:
        kb.insert(types.InlineKeyboardButton(
            f"{bundle.coin.ticker} - {bundle.exchange1.name} 🔄 {bundle.exchange2.name}",
            callback_data=f'{MODULE_NAME}:{Steps.DELETE_BUNDLE}:{bundle.id}'
        ))

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{Steps.DELETE_BUNDLE}'))

    text = f"{mc.BUNDLES_TITLE}{mc.LINE}{mc.BUNDLES_DELETE_BUNDLE}"

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(MODULE_NAME))
async def callback(callback_query: types.CallbackQuery):
    """
    Функция обработки нажатий на кнопки в стартовом меню
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    if Steps.BACK in callback_info:
        if callback_info == Steps.BACK:
            await start.start_menu(message=callback_query.message, edit=True)
        else:
            await bundles_menu(message=callback_query.message)
    elif Steps.ADD_BUNDLE in callback_info:
        if callback_info == Steps.ADD_BUNDLE:
            await chose_bundle_coin(message=callback_query.message)
        else:
            callback_info = callback_info.replace(f'{Steps.ADD_BUNDLE}:', '')
            if ':' in callback_info:
                telegram_id = str(callback_query.message.chat.id)
                coin_id, bundle_id = map(int, callback_info.split(':'))
                await user_api.add_user_bundle(telegram_id=telegram_id, data=schemas.UserBundleAdd(bundle_id=bundle_id))
                await bundles_menu(message=callback_query.message)
            else:
                coin_id = int(callback_info)
                await chose_bundle(message=callback_query.message, coin_id=coin_id)
    elif Steps.DELETE_BUNDLE in callback_info:
        telegram_id = str(callback_query.message.chat.id)
        if callback_info == Steps.DELETE_BUNDLE:
            await chose_delete_bundle(message=callback_query.message, telegram_id=telegram_id)
        else:
            bundle_id = int(callback_info.replace(f'{Steps.DELETE_BUNDLE}:', ''))
            await user_api.delete_user_bundle(telegram_id=telegram_id, bundle_id=bundle_id)
            await bundles_menu(message=callback_query.message)
