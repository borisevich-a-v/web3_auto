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
    hash: Optional[HexStr] = None
    datetime_of_perform: Optional[datetime] = None  # todo rename
    contract_address: Optional[HexStr] = None
    application: Applications
    amount_in_usd: float
    from_: Enum
    to_: Enum  # "nft" if it is nft


class AccountDB(BaseModel):
    id_: str
    public_key: str
    next_transaction_datetime: datetime
