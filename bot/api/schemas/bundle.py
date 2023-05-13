"""
Модуль схем связок.
"""
from .base import APIBase
from .coin import CoinInDb
from .exchange import ExchangeInDb


class BundleInDb(APIBase):
    id: int

    coin: CoinInDb
    exchange1: ExchangeInDb
    exchange2: ExchangeInDb
