from decimal import Decimal
from typing import Any, List

from boto3.dynamodb.conditions import Attr
from eth_typing import HexStr
from interfaces import ITxRepository
from models import TxDB

TX_TABLE_NAME = "transactions"


def _txdb_to_dynamodb(txdb: TxDB) -> dict[str, Any]:  # todo implement with pydantic
    return {
        "id": txdb.id,
        "hash": str(txdb.hash),
        "chain": str(txdb.chain),
        "tx_date": txdb.tx_date.isoformat(),
        "account_public_key": str(txdb.account_public_key),
        "app": str(txdb.app),
        "amount_in_usd": Decimal(txdb.amount_in_usd),
        "amount": Decimal(txdb.amount),
        "from_token": str(txdb.from_token),  # TODO: it writes an address, I want to see name of token
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
