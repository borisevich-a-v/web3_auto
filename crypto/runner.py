from typing import List

from account import Account
from activities import Activities
from configs import RandomConfig


class Runner:
    def __init__(
        self,
        db,
        queue,
    ) -> None:
        self._db = db
        self.queue = queue
        self.rnd = RandomConfig()
        self.activities = Activities

    def _get_accounts_to_be_run(self) -> List[Account]:
        acc = Account(public_key="0x0944F692859Ae4398cC6351A1cE99BF5Fc0E22aD", rnd=self.rnd)
        accounts = [acc]
        return accounts

    def set_next_transaction_date(self):
        ...

    def run(self):
        while True:
            for account in self._get_accounts_to_be_run():
                account._perform_activity()
                self.set_next_transaction_date()

            self.rnd.sleep_between_runs()
