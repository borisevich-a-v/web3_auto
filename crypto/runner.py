from typing import List

from account import Account
from activities import Activities
from configs import RandomConfig
from eth_typing import HexStr
from repositories.account import IAccountRepository
from repositories.transactions import ITxRepository
from utils.random_values import get_random_datetime_in_future


class Runner:
    def __init__(
        self,
        account_repository: IAccountRepository,
        tx_repository: ITxRepository,
    ) -> None:
        self._account_repository = account_repository
        self._tx_repository = tx_repository
        self.rnd = RandomConfig()
        self.activities = Activities

    def _get_accounts_to_be_run(self) -> List[Account]:
        acc = Account(public_key="0x0944F692859Ae4398cC6351A1cE99BF5Fc0E22aD", rnd=self.rnd)
        accounts = [acc]
        return accounts

    def set_next_transaction_date(self, account_public_key: HexStr) -> None:
        next_tx_datetime = get_random_datetime_in_future(days_from=5, days_up_to=10, hours_up_to=1)
        self._account_repository.update_tx_date(account_public_key, next_tx_datetime)

    def run(self):
        for account in self._get_accounts_to_be_run():
            print(f"Making tx for {account}")
            account.perform_activity()
            self.set_next_transaction_date(account.public_key)

            self.rnd.sleep_between_accounts()
