"""
Модуль арбитражных ситуаций пользователя
"""
from datetime import datetime

from aiogram import types

from . import start
from .. import dp
from ..consts import (
    messages as mc,
    buttons as bc
)
from ..api import user as user_api


MODULE_NAME = 'my_arbi_events'


class Steps:
    BACK = 'back'


async def my_arbi_events_menu(message: types.Message):
    """
    Функция обработки меню арбитражных ситуаций пользователя
    """
    arbi_events = await user_api.get_arbi_events(telegram_id=str(message.chat.id))

    kb = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(bc.BACK, callback_data=f'{MODULE_NAME}:{Steps.BACK}')
    )

    text = f"{mc.MY_ARBI_EVENTS_TITLE}\n" \
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

    await message.edit_text(text=text, reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(MODULE_NAME))
async def callback(callback_query: types.CallbackQuery):
    """
    Функция обработки нажатий на кнопки в меню арбитражных ситуаций пользователя
    """
    callback_info = callback_query.data.replace(f'{MODULE_NAME}:', '')

    if callback_info == Steps.BACK:
        await start.start_menu(message=callback_query.message, edit=True)
