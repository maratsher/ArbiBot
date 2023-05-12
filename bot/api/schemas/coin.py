"""
Модуль схем монеты.
"""
from .base import APIBase


class CoinInDb(APIBase):
    id: int

    name: str
    ticker: str
