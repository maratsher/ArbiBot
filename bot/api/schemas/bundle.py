"""
Модуль схем связок.
"""
from .base import APIBase


class BundleInDb(APIBase):
    id: int

    coin_id: int
    exchange1_id: int
    exchange2_id: int
