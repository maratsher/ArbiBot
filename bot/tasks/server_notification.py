import datetime
import json
import typing

import asyncio
from aiogram import types

from .. import bot, sender
from ..consts import messages as mc


async def new_event_message(telegram_ids: typing.List[str], data: dict):
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


async def stop_message(telegram_id: str):
    await bot.send_message(chat_id=telegram_id, text=mc.STOP_AUTO_NOTIFICATION, parse_mode=types.ParseMode.HTML)


async def restart_message(telegram_id: str):
    await bot.send_message(chat_id=telegram_id, text=mc.RESTART_AUTO_NOTIFICATION, parse_mode=types.ParseMode.HTML)


async def profit_message(telegram_id: str, profit: float):
    await bot.send_message(
        chat_id=telegram_id, text=mc.PROFIT_NOTIFICATION.format(profit=profit), parse_mode=types.ParseMode.HTML
    )


async def order_not_executed_time_message(telegram_id: str, exchange: str, order: str, time: str):
    await bot.send_message(
        chat_id=telegram_id,
        text=mc.ORDER_NOT_EXECUTED_TIME_NOTIFICATION.format(
            exchange=exchange,
            order=order,
            time=time
        ),
        parse_mode=types.ParseMode.HTML
    )


async def debug_message(telegram_id: str, debug_type: str, message: str):
    if debug_type == 'INFO':
        notification = mc.INFO_DEBUG_NOTIFICATION
    elif debug_type == 'WARNING':
        notification = mc.WARNING_DEBUG_NOTIFICATION
    else:
        notification = mc.ERROR_DEBUG_NOTIFICATION
    await bot.send_message(
        chat_id=telegram_id, text=notification.format(message=message), parse_mode=types.ParseMode.HTML
    )


@sender.task(name='new_event')
def new_event(telegram_ids: typing.List[str], message: str):
    asyncio.get_event_loop().run_until_complete(new_event_message(telegram_ids=telegram_ids, data=json.loads(message)))


@sender.task(name='stop_auto')
def stop_auto(telegram_id: str):
    asyncio.get_event_loop().run_until_complete(stop_message(telegram_id=telegram_id))


@sender.task(name='restart_auto')
def restart_auto(telegram_id: str):
    asyncio.get_event_loop().run_until_complete(restart_message(telegram_id=telegram_id))


@sender.task(name='profit')
def profit_auto(telegram_id: str, profit: float):
    asyncio.get_event_loop().run_until_complete(profit_message(telegram_id=telegram_id, profit=profit))


@sender.task(name='order_not_executed_time')
def order_not_executed_time(telegram_id: str, exchange: str, order: str, time: str):
    asyncio.get_event_loop().run_until_complete(
        order_not_executed_time_message(telegram_id=telegram_id, exchange=exchange, order=order, time=time)
    )


@sender.task(name='debug')
def debug(telegram_id: str, debug_type: str, message: str):
    asyncio.get_event_loop().run_until_complete(debug_message(
        telegram_id=telegram_id, debug_type=debug_type, message=message
    ))
