"""
Модуль схем бирж.
"""
from .base import APIBase


class ExchangeInDb(APIBase):
    id: int

    exchange_name: str
