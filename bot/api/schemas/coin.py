"""
Модуль схем монеты.
"""
from .base import APIBase


class CoinInDb(APIBase):
    id: int

    coin_name: str
    coin_ticker: str
