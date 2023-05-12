"""
Основной модуль бота.
"""
import time

from celery import Celery
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

sender = Celery(
    'bot',
    broker=f'redis://:{base_config.REDIS_PASSWORD}@{base_config.REDIS_HOST}:{base_config.REDIS_PORT}',
    backend=f'redis://:{base_config.REDIS_PASSWORD}@{base_config.REDIS_HOST}:{base_config.REDIS_PORT}',
    include=['bot.tasks.server_notification']
)

sender.conf.update(result_expires=3600)
