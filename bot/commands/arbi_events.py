"""
Модуль арбитражных ситуаций
"""
from datetime import datetime

from aiogram import types

from . import start
from .. import dp
from ..consts import (
    messages as mc,
    buttons as bc
)
from ..api import (
    user as user_api,
    arbi_event as arbi_event_api
)


MODULE_NAME = 'arbi_events'


class Steps:
    MY_BUNDLES = 'my_bundles'
    BACK = 'back'


async def arbi_events_menu(message: types.Message):
    """
    Функция обработки меню арбитражных ситуаций
    """
    arbi_events = await arbi_event_api.get_arbi_events(telegram_id=str(message.chat.id))

    bundle_stats = {}

    for event in arbi_events:
        if event.end:
            if event.bundle.id not in bundle_stats:
                bundle_stats[event.bundle.id] = {
                    'bundle': event.bundle,
                    'count': 0,
                    'time': 0,
                    'max_profit': 0
                }

            start_datetime = datetime.strptime(event.start, '%Y-%m-%dT%H:%M:%S.%f')
            end_datetime = datetime.strptime(event.end, '%Y-%m-%dT%H:%M:%S.%f')
            minutes = (end_datetime - start_datetime).seconds // 60

            bundle_stats[event.bundle.id]['count'] += 1
            bundle_stats[event.bundle.id]['time'] += minutes
            bundle_stats[event.bundle.id]['max_profit'] += event.max_profit

    kb = types.InlineKeyboardMarkup(row_width=1)

    text = f"{mc.ARBI_EVENTS_TITLE}\n" \
           f"<i>на {datetime.now().strftime('%d.%m.%Y')}</i>" \
           f"{mc.LINE}"

    if arbi_events:
        kb.add(types.InlineKeyboardButton(bc.MY_BUNDLES, callback_data=f'{MODULE_NAME}:{Steps.MY_BUNDLES}'))

    if bundle_stats:
        user = await user_api.get_user(telegram_id=str(message.chat.id))
        bace_coin_ticker = user.base_coin.ticker
        for num, bundle_stat in enumerate(bundle_stats.values()):
            bundle = bundle_stat['bundle']
            bundle_count = bundle_stat['count']
            text += f"<b>{num + 1}. {bundle.coin.ticker} / {bace_coin_ticker} - " \
                    f"{bundle.exchange1.name} 🔄 {bundle.exchange2.name}</b>\n" \
                    f"    Кол-во ситуаций: <b>{bundle_count}</b>\n" \
                    f"    Среднее время: <b>{bundle_stat['time'] / bundle_count:.2f} мин.</b>\n" \
                    f"    Средний профит: <b>{bundle_stat['max_profit'] / bundle_count:.2f} {bace_coin_ticker}</b>\n"
    else:
        text += mc.ARBI_EVENTS_EMPTY

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}'))

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


async def user_arbi_events_menu(message: types.Message):
    """
    Функция обработки меню арбитражных ситуаций пользователя
    """
    arbi_events = await user_api.get_arbi_events(telegram_id=str(message.chat.id))

    kb = types.InlineKeyboardMarkup(row_width=1)

    text = f"{mc.ARBI_EVENTS_TITLE}\n" \
           f"<i>на {datetime.now().strftime('%d.%m.%Y')}</i>" \
           f"{mc.LINE}"

    if arbi_events:
        user = await user_api.get_user(telegram_id=str(message.chat.id))
        bace_coin_ticker = user.base_coin.ticker
        for event in arbi_events:
            ticker = event.bundle.coin.ticker
            first_price = event.current_price1
            second_price = event.current_price2

            start_datetime = datetime.strptime(event.start, '%Y-%m-%dT%H:%M:%S.%f')
            start_time = start_datetime.strftime('%H:%M')

            if event.end:
                end_datetime = datetime.strptime(event.end, '%Y-%m-%dT%H:%M:%S.%f')
                end_time = end_datetime.strftime('%H:%M')
                seconds = (end_datetime - start_datetime).seconds
                minutes = f"{seconds // 60} мин." if seconds >= 60 else ''
                seconds = f"{seconds % 60} сек." if seconds % 60 else ''
                time = f"(<i>{minutes}{' ' if minutes else ''}{seconds}</i>)"
            else:
                end_time = '...'
                time = ''

            direction = '➡️' if first_price < second_price else '⬅️'

            text += f"⏱ <b>{start_time} - {end_time}</b> {time}\n" \
                    f"<b>{ticker} / {bace_coin_ticker}</b>\n" \
                    f"<b>{event.bundle.exchange1.name}</b> (<b>{first_price:.4f}</b>) " \
                    f"{direction} " \
                    f"<b>{event.bundle.exchange2.name}</b> (<b>{second_price:.4f}</b>)\n" \
                    f"<b>Профит:</b> от <b>{event.min_profit:.2f}</b> до <b>{event.max_profit:.2f}</b>\n\n"
    else:
        text += mc.ARBI_EVENTS_EMPTY

    kb.add(types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}:{Steps.MY_BUNDLES}'))

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
            await arbi_events_menu(message=callback_query.message)
    elif callback_info == Steps.MY_BUNDLES:
        await user_arbi_events_menu(message=callback_query.message)
