from datetime import datetime
from typing import List

from .configs import Activities, RandomConfig
from .crypto.swap_factory import SwapFactory
from .db import Account, Applications, Tx

app_to_activities_map: dict[Applications, SwapFactory] = {Applications: Activities.SYNCSWAP.value}


class Runner:
    def __init__(self, db, queue, rnd: RandomConfig, activities: Activities) -> None:
        self._db = db
        self.queue = queue
        self.rnd = rnd
        self.activities = activities

    def _get_accounts_to_be_run(self) -> List[Account]:
        accounts = self._db.search()
        return accounts

    def _calculate_next_transaction(self, account: Account) -> Tx:
        tx = Tx()
        return tx

    def get_private_key_for_acc(self, account: Account) -> str:
        ...

    def convert_usd_to_token(self, usd_amount, token) -> int:
        return int(1.1)

    def set_busy(self, account):
        ...

    def release_busy(self, account):
        ...

    def save_tx(self, tx):
        ...

    def _perform_activity(self, account: Account) -> None:
        tx = self._calculate_next_transaction(account)
        swap_factory = app_to_activities_map[tx.application]
        swap_factory.get_swap(
            private_key=self.get_private_key_for_acc(account),
            from_token=tx.from_,
            to_token=tx.to_,
            amount_to_swap=self.convert_usd_to_token(tx.amount_in_usd, tx.from_),
        ).swap()
        self.save_tx(tx)

    def set_next_transaction_date(self):
        ...

    def run(self):
        while True:
            for account in self._get_accounts_to_be_run():
                self._perform_activity(account)
                self.set_next_transaction_date()

            self.rnd.sleep_between_runs()
