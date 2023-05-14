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
    BACK = 'back'


async def bundles_rating_menu(message: types.Message):
    """
    Функция обработки меню рейтинга связок
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

    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
    )

    text = f"{mc.BUNDLES_RATING_TITLE}\n" \
           f"<i>на {datetime.now().strftime('%d.%m.%Y')}</i>" \
           f"{mc.LINE}"

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

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(MODULE_NAME))
async def callback(callback_query: types.CallbackQuery):
    """
    Функция обработки нажатий на кнопки в меню рейтинга связок
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    if callback_info == Steps.BACK:
        await start.start_menu(message=callback_query.message, edit=True)
