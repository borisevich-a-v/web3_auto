from datetime import datetime
from typing import List, Optional

from boto3.dynamodb.conditions import Attr
from eth_typing import HexStr
from interfaces import IAccountRepository
from models import AccountDB

ACCOUNT_TABLE_NAME = "accounts"


class AccountRepository(IAccountRepository):
    def __init__(self, dynamodb) -> None:
        self.table = dynamodb.Table(ACCOUNT_TABLE_NAME)

    def get(self, public_key) -> AccountDB:
        response = self.table.get_item(Key={"public_key": public_key})
        return AccountDB.model_validate(response["Item"])

    def get_by_next_tx_date(self, next_tx_date: Optional[datetime] = None) -> List[AccountDB]:
        if not next_tx_date:
            next_tx_date = datetime.now()
        response = self.table.scan(
            Select="ALL_ATTRIBUTES",
            FilterExpression=Attr("next_tx_date").lte(next_tx_date.isoformat()),
        )
        print(response["Items"])
        return [AccountDB.model_validate(acc) for acc in response["Items"]]

    def update_tx_date(self, public_key: HexStr, next_tx_date: datetime) -> AccountDB:
        return self.put_account(AccountDB(public_key=public_key, next_tx_date=next_tx_date))

    def put_account(self, account_db: AccountDB) -> AccountDB:
        self.table.put_item(
            Item={"public_key": account_db.public_key, "next_tx_date": account_db.next_tx_date.isoformat()}
        )
        return account_db
