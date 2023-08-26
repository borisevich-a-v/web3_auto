from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from boto3.dynamodb.conditions import Attr
from eth_typing import HexStr
from pydantic import BaseModel

ACCOUNT_TABLE_NAME = "accounts"


class AccountDB(BaseModel):
    public_key: HexStr
    next_tx_date: datetime


class IAccountRepository(ABC):
    @abstractmethod
    def get(self, public_key) -> AccountDB:
        ...

    @abstractmethod
    def get_by_next_tx_date(self, next_tx_date: datetime = datetime.now()) -> List[AccountDB]:
        ...

    @abstractmethod
    def update_tx_date(self, public_key: HexStr, next_tx_date: datetime) -> AccountDB:
        ...

    @abstractmethod
    def put_account(self, account_db: AccountDB) -> AccountDB:
        ...


class AccountRepository(IAccountRepository):
    def __init__(self, dynamodb) -> None:
        self.table = dynamodb.Table(ACCOUNT_TABLE_NAME)

    def get(self, public_key) -> AccountDB:
        response = self.table.get_item(Key={"public_key": public_key})
        return response["Item"]

    def get_by_next_tx_date(self, next_tx_date: datetime = datetime.now()) -> List[AccountDB]:
        response = self.table.scan(
            Select="ALL_ATTRIBUTES",
            FilterExpression=Attr("next_tx_date").lte(next_tx_date.isoformat()),
        )
        return [AccountDB.model_validate(acc) for acc in response["Items"]]

    def update_tx_date(self, public_key: HexStr, next_tx_date: datetime) -> AccountDB:
        return self.put_account(AccountDB(public_key=public_key, next_tx_date=next_tx_date))

    def put_account(self, account_db: AccountDB) -> AccountDB:
        self.table.put_item(
            Item={"public_key": account_db.public_key, "next_tx_date": account_db.next_tx_date.isoformat()}
        )
        return account_db
