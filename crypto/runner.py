from typing import List

from activities import Activities
from configs import RandomConfig, settings
from eth_typing import HexStr
from executor import Executor
from models import AccountDB
from repositories.account import IAccountRepository
from repositories.transactions import ITxRepository

from utils.random_values import get_random_datetime_in_future


class Runner:
    def __init__(
        self,
        account_repository: IAccountRepository,
        tx_repository: ITxRepository,
        secret_manager: ...,
        random_config: RandomConfig,
        activities: Activities,
    ) -> None:
        self._account_repository = account_repository
        self._tx_repository = tx_repository
        self._secret_manager = secret_manager
        self.rnd = random_config
        self.activities = activities

    def _get_accounts_to_be_run(self) -> List[AccountDB]:
        print("getting account to run")
        # return self._account_repository.get_by_next_tx_date(datetime.datetime(year=1999, month=1, day=1))
        return [self._account_repository.get(settings.public_key)]

    def set_next_transaction_date(self, account_public_key: HexStr) -> None:
        next_tx_datetime = get_random_datetime_in_future(days_from=5, days_up_to=10, hours_up_to=1)
        self._account_repository.update_tx_date(account_public_key, next_tx_datetime)

    def run(self):
        for account in self._get_accounts_to_be_run():
            print(f"Making tx for {account}")
            executor = Executor(account.public_key, self.rnd, self._tx_repository, self._secret_manager)
            executor.perform_activity()

            self.set_next_transaction_date(account.public_key)

            self.rnd.sleep_between_accounts()
        print("All accounts were done")
