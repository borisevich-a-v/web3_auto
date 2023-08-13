import random

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    private_key: str


class RandomConfig(BaseSettings):
    _delay_after_approve_from = 1
    _delay_after_approve_till = 30

    @property
    def delay_after_approve(self) -> float:
        return (1 + random.betavariate(alpha=2, beta=5)) * (
            self._delay_after_approve_from / self._delay_after_approve_till
        )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
rnd = RandomConfig()
