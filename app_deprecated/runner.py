import datetime
import logging
from typing import List

from activities import Activities
from eth_typing import HexStr
from executor import Executor
from infrastructure.repositories.transactions import ITxRepository
from interfaces import IAccountRepository
from models import AccountDB
from utils.random_values import get_random_datetime_in_future

from app.configs import RandomConfig

logger = logging.getLogger()


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
        logger.info("Retrieving accounts to be run")
        return self._account_repository.get_by_next_tx_date(datetime.datetime(year=2099, month=1, day=1))  # TODO

    def set_next_transaction_date(self, account_public_key: HexStr) -> None:
        next_tx_datetime = get_random_datetime_in_future(days_from=5, days_up_to=10, hours_up_to=1)
        logger.info("Next transaction date is %s", str(next_tx_datetime))
        self._account_repository.update_tx_date(account_public_key, next_tx_datetime)

    def run(self):
        for account in self._get_accounts_to_be_run():
            logger.info("Executing transactions for %s", account.public_key)
            executor = Executor(account.public_key, self.rnd, self._tx_repository, self._secret_manager)
            executor.perform_activity()

            self.set_next_transaction_date(account.public_key)

            self.rnd.sleep_between_accounts()
        print("All accounts were done")
