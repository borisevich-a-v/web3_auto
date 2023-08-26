import random
import time

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from utils.random_values import get_random_value_with_2_5_betavariate


class Settings(BaseSettings):
    private_key: str

    aws_access_key: str
    aws_secret_key: str
    aws_region: str


class RandomConfig(BaseModel):
    _delay_after_approve_from = 0.5
    _delay_after_approve_upto = 30

    _delay_between_runs_from = 1
    _delay_between_runs_upto = 2  # 15 * 60

    _delay_between_accounts_from = 1
    _delay_between_accounts_up_to = 2  # 5 * 60

    def sleep_after_approve(self) -> None:
        time_to_sleep = get_random_value_with_2_5_betavariate(
            self._delay_after_approve_from, self._delay_after_approve_upto
        )
        time.sleep(time_to_sleep)

    def sleep_between_accounts(self) -> None:
        time_to_sleep = get_random_value_with_2_5_betavariate(
            self._delay_between_accounts_from, self._delay_between_accounts_up_to
        )
        time.sleep(time_to_sleep)

    def sleep_between_runs(self) -> None:
        time_to_sleep = random.uniform(self._delay_between_runs_from, self._delay_between_runs_upto)
        time.sleep(time_to_sleep)


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
