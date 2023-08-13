import random
import time
from enum import Enum

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from crypto.crypto.swap_factory import SwapFactory
from crypto.crypto.syncswap_factory import SyncswapFactory


class Settings(BaseSettings):
    private_key: str

    dynamo_db_login: str
    dynamo_db_password: str

    worker_queue_name: str


class RandomConfig(BaseModel):
    _delay_after_approve_from = 1
    _delay_after_approve_upto = 30

    _delay_between_runs_from = 10 * 60
    _delay_between_runs_upto = 3 * 60 * 60

    def delay_after_approve(self) -> None:
        time_to_sleep = 1 + random.betavariate(alpha=2, beta=5) * (
            self._delay_after_approve_from / self._delay_after_approve_upto
        )
        time.sleep(time_to_sleep)

    def sleep_between_runs(self) -> None:
        time_to_sleep = random.uniform(self._delay_between_runs_from, self._delay_between_runs_upto)
        time.sleep(time_to_sleep)


class Activities(Enum):
    SYNCSWAP: SwapFactory = SyncswapFactory
