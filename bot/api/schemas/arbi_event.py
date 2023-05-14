"""
Модуль схем арбитражной ситуации.
"""
from .base import APIBase
from .coin import CoinInDb
from .bundle import BundleInDb


class ArbiEventInDb(APIBase):
    id: int

    start: str
    end: str | None

    bundle: BundleInDb

    min_profit: float
    max_profit: float
    current_price1: float
    current_price2: float
    used_base_coin: CoinInDb
    used_threshold: float
    used_volume: float
