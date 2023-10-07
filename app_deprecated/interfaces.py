from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from eth_typing import HexStr
from models import AccountDB, TxDB


class IAccountRepository(ABC):
    @abstractmethod
    def get(self, public_key) -> AccountDB:
        ...

    @abstractmethod
    def get_by_next_tx_date(self, next_tx_date: datetime = None) -> List[AccountDB]:
        ...

    @abstractmethod
    def update_tx_date(self, public_key: HexStr, next_tx_date: datetime) -> AccountDB:
        ...

    @abstractmethod
    def put_account(self, account_db: AccountDB) -> AccountDB:
        ...


class ITxRepository(ABC):
    @abstractmethod
    def count_txs_for_account(self, public_key: HexStr) -> int:
        ...

    @abstractmethod
    def get_account_txs(self, public_key: HexStr) -> List[TxDB]:
        ...

    @abstractmethod
    def post_tx(self, tx: TxDB) -> TxDB:
        ...
