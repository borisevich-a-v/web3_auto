from abc import ABC
from enum import Enum


class Swap(ABC):
    def swap(self) -> None:
        ...


class SwapFactory:
    @classmethod
    def get_swap(cls, private_key: str, from_token: Enum, to_token: Enum, amount_to_swap: float) -> Swap:
        ...
