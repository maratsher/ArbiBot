"""
Модуль схем пользователя.
"""
from pydantic import Field

from .base import APIBase
from .coin import CoinInDb
from ..config import db_config


class UserInDb(APIBase):
    id: int

    telegram_id: str
    base_coin: CoinInDb
    threshold: float
    volume: float


class UserCreate(APIBase):
    telegram_id: str = Field(...)


class UserBundleAdd(APIBase):
    bundle_id: int = Field(..., ge=1, le=db_config.MAX_LEN_ID)


class UserBaseCoinUpdate(APIBase):
    telegram_id: str = Field(...)

    base_coin_id: int = Field(..., ge=1, le=db_config.MAX_LEN_ID)


class UserThresholdUpdate(APIBase):
    telegram_id: str = Field(...)

    threshold: float = Field(..., gt=0, le=db_config.MAX_THRESHOLD)


class UserVolumeUpdate(APIBase):
    telegram_id: str = Field(...)

    volume: float = Field(..., gt=0, le=db_config.MAX_VOLUME)
