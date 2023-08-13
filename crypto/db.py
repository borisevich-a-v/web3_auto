from datetime import datetime
from enum import Enum
from typing import Optional

from eth_typing import HexStr
from pydantic import BaseModel


class Applications(Enum):  # The same as activities?
    SYNCSWAP = "syncswap"


class Tx(BaseModel):
    id_: str
    account_id: str
    hash: HexStr
    datetime_of_perform: Optional[datetime]  # todo rename
    contract_address: Optional[HexStr]
    application: Applications
    amount_in_usd: float
    from_: str
    to_: str  # "nft" if it is nft


class Account(BaseModel):
    id_: str
    public_key: str
    busy: bool
    next_transaction_datetime: datetime
