"""
Модуль настроек
"""
from re import fullmatch

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from . import start
from .. import dp
from ..consts import (
    messages as mc,
    buttons as bc,
    regex as rc,
    errors as ec
)
from ..api import (
    user as user_api,
    coin as coin_api,
    schemas
)


MODULE_NAME = 'settings'


class Steps:
    UPDATE_BASE_COIN = 'update_base_coin'
    UPDATE_VOLUME = 'update_volume'
    UPDATE_THRESHOLD = 'update_threshold'
    BACK = 'back'


class StorageDataFields:
    LAST_MESSAGE = 'last_bot_message'


class SettingsForm(StatesGroup):
    get_volume = State()
    get_threshold = State()


async def settings_menu(message: types.Message):
    """
    Функция обработки меню настроек
    """
    user = await user_api.get_user(telegram_id=str(message.chat.id))

    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(bc.UPDATE_BASE_COIN, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_BASE_COIN}'),
        types.InlineKeyboardButton(bc.UPDATE_VOLUME, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_VOLUME}'),
        types.InlineKeyboardButton(bc.UPDATE_THRESHOLD, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_THRESHOLD}'),
        types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
    )

    settings_info = mc.SETTINGS_INFO.format(
        base_coin_name=f"{user.base_coin.name} ({user.base_coin.ticker})",
        volume=f"{user.volume} {user.base_coin.ticker}",
        threshold=f"{user.threshold} {user.base_coin.ticker}"
    )

    text = f"{mc.SETTINGS_TITLE}{mc.LINE}{settings_info}"

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


async def chose_new_base_coin(message: types.Message):
    """
    Функция обработки меню выбора новой расчетной монеты
    """
    coins = await coin_api.get_coins()

    kb = types.InlineKeyboardMarkup(row_width=3)

    for coin in coins:
        kb.insert(types.InlineKeyboardButton(
            coin.ticker, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_BASE_COIN}:{coin.id}'
        ))

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{MODULE_NAME}'))

    text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_BASE_COIN}"

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.message_handler(state=SettingsForm.get_volume)
async def get_volume(message: types.Message, state: FSMContext):
    """
    Функция обновления объема торгов пользователя
    """
    volume = message.text

    await message.delete()

    telegram_id = message.chat.id
    data = await state.storage.get_data(chat=telegram_id)

    if fullmatch(rc.FLOAT_REGEX, volume):
        volume = volume.replace(',', '.')
        await user_api.update_volume(data=schemas.UserVolumeUpdate(telegram_id=str(telegram_id), volume=volume))
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_VOLUME}\n\n{ec.INPUT_FORMAT.format(mc.FLOAT_FORMAT)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.message_handler(state=SettingsForm.get_threshold)
async def get_threshold(message: types.Message, state: FSMContext):
    """
    Функция обновления порога арбитражной ситуации пользователя
    """
    threshold = message.text

    await message.delete()

    telegram_id = message.chat.id
    data = await state.storage.get_data(chat=telegram_id)

    if fullmatch(rc.FLOAT_REGEX, threshold):
        threshold = threshold.replace(',', '.')
        await user_api.update_threshold(
            data=schemas.UserThresholdUpdate(telegram_id=str(telegram_id), threshold=threshold)
        )
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_THRESHOLD}\n\n{ec.INPUT_FORMAT.format(mc.FLOAT_FORMAT)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith(MODULE_NAME),
    state=[SettingsForm.get_volume, SettingsForm.get_threshold, None]
)
async def callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатий на кнопки в меню настроек
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    text, kb = None, None

    if Steps.BACK in callback_info:
        if callback_info == Steps.BACK:
            await start.start_menu(message=callback_query.message, edit=True)
        else:
            await settings_menu(callback_query.message)

        current_state = await state.get_state()
        if current_state:
            await state.finish()
    elif Steps.UPDATE_BASE_COIN in callback_info:
        if callback_info == Steps.UPDATE_BASE_COIN:
            await chose_new_base_coin(message=callback_query.message)
        else:
            telegram_id = str(callback_query.message.chat.id)
            base_coin_id = int(callback_info.replace(f'{Steps.UPDATE_BASE_COIN}:', ''))
            await user_api.update_base_coin(
                data=schemas.UserBaseCoinUpdate(telegram_id=telegram_id, base_coin_id=base_coin_id)
            )
            await settings_menu(message=callback_query.message)
    elif callback_info in [Steps.UPDATE_VOLUME, Steps.UPDATE_THRESHOLD]:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}" \
               f"{mc.SETTINGS_VOLUME if callback_info == Steps.UPDATE_VOLUME else mc.SETTINGS_THRESHOLD}" \
               f"\n\n{mc.INPUT_FORMAT.format(mc.FLOAT_FORMAT)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{MODULE_NAME}')
        )
        if callback_info == Steps.UPDATE_VOLUME:
            await SettingsForm.get_volume.set()
        else:
            await SettingsForm.get_threshold.set()

    if text:
        msg = await callback_query.message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})
