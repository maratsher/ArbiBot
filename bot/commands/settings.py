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
from ..api.config import db_config


MODULE_NAME = 'settings'


class Steps:
    UPDATE_AUTO = 'update_auto'
    UPDATE_BASE_COIN = 'update_base_coin'
    UPDATE_VOLUME = 'update_volume'
    UPDATE_THRESHOLD = 'update_threshold'
    UPDATE_EPSILON = 'update_epsilon'
    UPDATE_DIFFERENCE = 'update_difference'
    UPDATE_WAIT_ORDER = 'update_wait_order'
    UPDATE_TEST_API = 'update_test_api'
    BACK = 'back'


class StorageDataFields:
    LAST_MESSAGE = 'last_bot_message'


class SettingsForm(StatesGroup):
    get_volume = State()
    get_threshold = State()
    get_epsilon = State()
    get_difference = State()
    get_wait_order_minutes = State()


async def settings_menu(message: types.Message):
    """
    Функция обработки меню настроек
    """
    user = await user_api.get_user(telegram_id=str(message.chat.id))

    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(
            f'{"✅" if user.auto else "❌"} {bc.AUTO}',
            callback_data=f'{MODULE_NAME}:{Steps.UPDATE_AUTO}:{int(not user.auto)}'
        ),
        types.InlineKeyboardButton(
            f'{"✅" if user.test_api else "❌"} {bc.TEST}',
            callback_data=f'{MODULE_NAME}:{Steps.UPDATE_TEST_API}:{int(not user.test_api)}'
        ),
        types.InlineKeyboardButton(bc.UPDATE_BASE_COIN, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_BASE_COIN}'),
        types.InlineKeyboardButton(bc.UPDATE_VOLUME, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_VOLUME}'),
        types.InlineKeyboardButton(bc.UPDATE_THRESHOLD, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_THRESHOLD}'),
        types.InlineKeyboardButton(bc.UPDATE_EPSILON, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_EPSILON}'),
        types.InlineKeyboardButton(bc.UPDATE_DIFFERENCE, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_DIFFERENCE}'),
        types.InlineKeyboardButton(bc.UPDATE_WAIT_ORDER, callback_data=f'{MODULE_NAME}:{Steps.UPDATE_WAIT_ORDER}'),
        types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
    )

    settings_info = mc.SETTINGS_INFO.format(
        base_coin_name=f"{user.base_coin.name} ({user.base_coin.ticker})",
        volume=f"{user.volume} {user.base_coin.ticker}",
        threshold=f"{user.threshold} {user.base_coin.ticker}",
        epsilon=f"{user.epsilon} {user.base_coin.ticker}",
        difference=f"{user.difference} %",
        wait_order_minutes=f"{user.wait_order_minutes} мин."
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

    if fullmatch(rc.FLOAT_REGEX, volume) and float(volume.replace(',', '.')) <= db_config.MAX_VOLUME:
        volume = volume.replace(',', '.')
        await user_api.update_volume(data=schemas.UserVolumeUpdate(telegram_id=str(telegram_id), volume=volume))
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_VOLUME}\n\n" \
               f"{ec.INPUT_FORMAT.format(format=mc.FLOAT_FORMAT, max_value=db_config.MAX_VOLUME)}"
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

    if fullmatch(rc.FLOAT_REGEX, threshold) and float(threshold.replace(',', '.')) <= db_config.MAX_THRESHOLD:
        threshold = threshold.replace(',', '.')
        await user_api.update_threshold(
            data=schemas.UserThresholdUpdate(telegram_id=str(telegram_id), threshold=threshold)
        )
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_THRESHOLD}\n\n" \
               f"{ec.INPUT_FORMAT.format(format=mc.FLOAT_FORMAT, max_value=db_config.MAX_THRESHOLD)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.message_handler(state=SettingsForm.get_epsilon)
async def get_epsilon(message: types.Message, state: FSMContext):
    """
    Функция обновления погрешности сравнения цен пользователя
    """
    epsilon = message.text

    await message.delete()

    telegram_id = message.chat.id
    data = await state.storage.get_data(chat=telegram_id)

    if fullmatch(rc.FLOAT_REGEX, epsilon) and float(epsilon.replace(',', '.')) <= db_config.MAX_EPSILON:
        epsilon = epsilon.replace(',', '.')
        await user_api.update_epsilon(
            data=schemas.UserEpsilonUpdate(telegram_id=str(telegram_id), epsilon=epsilon)
        )
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_EPSILON}\n\n" \
               f"{ec.INPUT_FORMAT.format(format=mc.FLOAT_FORMAT, max_value=db_config.MAX_EPSILON)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.message_handler(state=SettingsForm.get_difference)
async def get_difference(message: types.Message, state: FSMContext):
    """
    Функция обновления максимально допустимого процента различия балансов пользователя
    """
    difference = message.text

    await message.delete()

    telegram_id = message.chat.id
    data = await state.storage.get_data(chat=telegram_id)

    if fullmatch(rc.FLOAT_REGEX, difference) and float(difference.replace(',', '.')) <= db_config.MAX_DIFFERENCE:
        difference = difference.replace(',', '.')
        await user_api.update_difference(
            data=schemas.UserDifferenceUpdate(telegram_id=str(telegram_id), difference=difference)
        )
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_DIFFERENCE}\n\n" \
               f"{ec.INPUT_FORMAT.format(format=mc.FLOAT_FORMAT, max_value=db_config.MAX_DIFFERENCE)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.message_handler(state=SettingsForm.get_wait_order_minutes)
async def get_wait_order_minutes(message: types.Message, state: FSMContext):
    """
    Функция обновления времени на выполнение ордера пользователя
    """
    wait_order_minutes = message.text

    await message.delete()

    telegram_id = message.chat.id
    data = await state.storage.get_data(chat=telegram_id)

    if fullmatch(rc.FLOAT_REGEX, wait_order_minutes) and float(wait_order_minutes.replace(',', '.')) <= db_config.MAX_WAIT_ORDER_MINUTES:
        wait_order_minutes = wait_order_minutes.replace(',', '.')
        await user_api.update_wait_order_minutes(
            data=schemas.UserWaitOrderMinutesUpdate(telegram_id=str(telegram_id), wait_order_minutes=wait_order_minutes)
        )
        await settings_menu(message=data[StorageDataFields.LAST_MESSAGE])
        await state.finish()
    else:
        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{mc.SETTINGS_WAIT_ORDER}\n\n" \
               f"{ec.INPUT_FORMAT.format(format=mc.INT_FORMAT, max_value=db_config.MAX_WAIT_ORDER_MINUTES)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
        )
        msg = await data[StorageDataFields.LAST_MESSAGE].edit_text(
            text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML
        )
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})


@dp.callback_query_handler(
    lambda c: c.data and c.data.startswith(MODULE_NAME),
    state=[SettingsForm, None]
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
    elif Steps.UPDATE_AUTO in callback_info:
        telegram_id = str(callback_query.message.chat.id)
        auto = int(callback_info.replace(f'{Steps.UPDATE_AUTO}:', ''))
        result = await user_api.update_auto(data=schemas.UserAutoUpdate(telegram_id=telegram_id, auto=auto))
        if result == 1:
            await callback_query.message.delete()
            await callback_query.message.answer(text=mc.SETTINGS_AUTO_STOP_PROCESS_STARTED)
        else:
            await settings_menu(message=callback_query.message)
    elif Steps.UPDATE_TEST_API in callback_info:
        telegram_id = str(callback_query.message.chat.id)
        test_api = int(callback_info.replace(f'{Steps.UPDATE_TEST_API}:', ''))
        result = await user_api.update_test_api(
            data=schemas.UserTestAPIUpdate(telegram_id=telegram_id, test_api=test_api)
        )
        if result == 1:
            await callback_query.message.delete()
            await callback_query.message.answer(text=mc.SETTINGS_AUTO_RESTART_PROCESS_STARTED)
        else:
            await settings_menu(message=callback_query.message)
    else:
        input_format = mc.FLOAT_FORMAT
        if callback_info == Steps.UPDATE_VOLUME:
            settings_info = mc.SETTINGS_VOLUME
            max_value = db_config.MAX_VOLUME
            await SettingsForm.get_volume.set()
        elif callback_info == Steps.UPDATE_THRESHOLD:
            settings_info = mc.SETTINGS_THRESHOLD
            max_value = db_config.MAX_THRESHOLD
            await SettingsForm.get_threshold.set()
        elif callback_info == Steps.UPDATE_EPSILON:
            settings_info = mc.SETTINGS_EPSILON
            max_value = db_config.MAX_EPSILON
            await SettingsForm.get_epsilon.set()
        elif callback_info == Steps.UPDATE_DIFFERENCE:
            settings_info = mc.SETTINGS_DIFFERENCE
            max_value = db_config.MAX_DIFFERENCE
            await SettingsForm.get_difference.set()
        elif callback_info == Steps.UPDATE_WAIT_ORDER:
            input_format = mc.INT_FORMAT
            settings_info = mc.SETTINGS_WAIT_ORDER
            max_value = db_config.MAX_WAIT_ORDER_MINUTES
            await SettingsForm.get_wait_order_minutes.set()
        else:
            return

        text = f"{mc.SETTINGS_TITLE}{mc.LINE}{settings_info}" \
               f"\n\n{mc.INPUT_FORMAT.format(format=input_format, max_value=max_value)}"
        kb = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{MODULE_NAME}')
        )

    if text:
        msg = await callback_query.message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)
        await state.update_data({StorageDataFields.LAST_MESSAGE: msg})
