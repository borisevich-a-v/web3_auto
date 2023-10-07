import uuid
from datetime import datetime
from enum import Enum

from eth_typing import HexStr
from pydantic import BaseModel, Field


class AccountDB(BaseModel):
    public_key: HexStr
    next_tx_date: datetime


class Tx(BaseModel):
    chain: str
    application: Enum
    amount: float
    from_token: Enum
    to_token: Enum


class TxDB(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hash: HexStr
    chain: str
    tx_date: datetime
    account_public_key: HexStr
    app: str
    amount_in_usd: float
    amount: float
    from_token: str  # ENUM
    to_token: str  # ENUM
