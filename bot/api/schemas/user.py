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
    epsilon: float
    difference: float
    auto: bool
    test_api: bool
    wait_order_minutes: int


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


class UserEpsilonUpdate(APIBase):
    telegram_id: str = Field(...)

    epsilon: float = Field(..., gt=0, le=db_config.MAX_EPSILON)


class UserDifferenceUpdate(APIBase):
    telegram_id: str = Field(...)

    difference: float = Field(..., gt=0, le=db_config.MAX_DIFFERENCE)


class UserAutoUpdate(APIBase):
    telegram_id: str = Field(...)

    auto: bool = Field(...)


class UserWaitOrderMinutesUpdate(APIBase):
    telegram_id: str = Field(...)

    wait_order_minutes: float = Field(..., gt=0, le=db_config.MAX_DIFFERENCE)


class UserTestAPIUpdate(APIBase):
    telegram_id: str = Field(...)

    test_api: bool = Field(...)


class UserExchangeUpdate(APIBase):
    telegram_id: str = Field(...)

    exchange_id: int = Field(..., ge=1, le=db_config.MAX_LEN_ID)

    api_key: str = Field(...)
    api_secret: str = Field(...)
