"""
Основной модуль бота.
"""
import time

from aiogram import Dispatcher

from bot.api import _base
from bot.consts import main as mc
from bot.config import base_config
from bot.utils.BotWrapper import BotWrapper


# connect to server
ping_server = _base.ping_server()
while not ping_server:
    time.sleep(mc.RETRY_DELAY_IN_SECONDS)
    ping_server = _base.ping_server()
print('Server connection established!')


bot = BotWrapper(token=base_config.BOT_TOKEN)
dp = Dispatcher(bot)
