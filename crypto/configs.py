import random
import time
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from utils.random_values import get_random_value_with_2_5_betavariate


class Settings(BaseSettings):
    local_public_key: Optional[str]
    local_private_key: Optional[str]

    aws_access_key: str = "admin"
    aws_secret_key: str = "admin"
    aws_region: str = "us-east"
    aws_endpoint_url: str = "localhost:8000"


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


settings = Settings(_env_file="../.env", _env_file_encoding="utf-8")
