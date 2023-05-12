"""
Модуль схем арбитражной ситуации.
"""
from .base import APIBase


class ArbiEventInDb(APIBase):
    id: int

    start: str
    end: str

    bundle_id: int
    min_profit: float
    max_profit: float
