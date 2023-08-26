import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List

from boto3.dynamodb.conditions import Attr
from eth_typing import HexStr
from pydantic import BaseModel

TX_TABLE_NAME = "transactions"


class TxDB(BaseModel):
    id_: str
    hash: HexStr
    chain: str
    tx_date: datetime
    account_public_key: HexStr
    contract_address: HexStr
    amount_in_usd: float
    amount: float
    from_token: str  # ENUM
    to_token: str  # ENUM


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


def _txdb_to_dynamodb(txdb: TxDB) -> dict[str, Any]:
    return {
        "id": uuid.uuid4(),
        "hash": str(txdb.hash),
        "chain": str(txdb.chain),
        "tx_date": txdb.tx_date.isoformat(),
        "account_public_key": str(txdb.account_public_key),
        "contract_address": str(txdb.contract_address),
        "amount_in_usd": float(txdb.amount_in_usd),
        "amount": float(txdb.amount),
        "from_token": str(txdb.from_token),
        "to_token": str(txdb.to_token),
    }


class TxRepository(ITxRepository):
    def __init__(self, dynamodb) -> None:
        self.table = dynamodb.Table(TX_TABLE_NAME)

    def count_txs_for_account(self, public_key: HexStr) -> int:
        response = self.table.scan(
            Select="COUNT",
            FilterExpression=Attr("account_public_key").eq(public_key),
        )
        return [TxDB.model_validate(acc) for acc in response["Items"]]

    def get_account_txs(self, public_key: HexStr) -> List[TxDB]:  # TODO create index for public_key
        response = self.table.scan(
            Select="ALL_ATTRIBUTES",
            FilterExpression=Attr("account_public_key").eq(public_key),
        )
        return [TxDB.model_validate(acc) for acc in response["Items"]]

    def post_tx(self, tx: TxDB) -> TxDB:
        self.table.put_item(Item=_txdb_to_dynamodb(tx))
