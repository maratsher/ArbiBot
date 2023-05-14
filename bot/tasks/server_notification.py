import json
import typing

import asyncio
from aiogram import types

from .. import bot, sender
from ..consts import messages as mc


async def send_message(telegram_ids: typing.List[str], data: dict):
    direction = '➡️' if data['current_price1'] < data['current_price2'] else '⬅️'
    text = mc.NEW_EVENT_NOTIFICATION.format(
        line=mc.LINE,
        ticker=data['ticker'],
        bace_coin_ticker=data['base_coin_ticker'],
        exchange1_name=data['exchange1'],
        first_price=float(data['current_price1']),
        direction=direction,
        exchange2_name=data['exchange2'],
        second_price=float(data['current_price2']),
        profit=float(data['profit'])
    )
    for telegram_id in set(telegram_ids):
        await bot.send_message(chat_id=telegram_id, text=text, parse_mode=types.ParseMode.HTML)


@sender.task(name='send_notification')
def send_notification(telegram_ids: typing.List[str], message: str):
    asyncio.get_event_loop().run_until_complete(send_message(telegram_ids=telegram_ids, data=json.loads(message)))
