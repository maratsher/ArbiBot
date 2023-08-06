"""
Модуль схем бирж.
"""
from enum import Enum

from .base import APIBase


class ExchangeName(str, Enum):
    """Список констант для Exchange.name"""
    BINANCE = 'Binance'
    BYBIT = 'Bybit'

    @classmethod
    def to_dict(cls):
        return {e.name: e.value for e in cls}


class ExchangeInDb(APIBase):
    id: int

    name: ExchangeName
