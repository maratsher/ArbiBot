import json
import typing

import asyncio
from aiogram import types

from .. import bot, sender


async def send_message(telegram_ids: typing.List[str], message: str):
    for telegram_id in set(telegram_ids):
        await bot.send_message(chat_id=telegram_id, text=message, parse_mode=types.ParseMode.HTML)


@sender.task(name='send_notification')
def send_notification(telegram_ids: typing.List[str], message: str):
    asyncio.get_event_loop().run_until_complete(send_message(telegram_ids=telegram_ids, message=message))
