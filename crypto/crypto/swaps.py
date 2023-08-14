from abc import ABC, abstractmethod
from enum import Enum

from eth_typing import HexStr
from pydantic import BaseModel


class Swap(ABC):

    @abstractmethod
    def __init__(self, private_key: str, from_token: Enum, to_token: Enum, amount_to_swap: float,
                 rnd: BaseModel) -> None:
        ...

    @abstractmethod
    def swap(self) -> HexStr:
        ...


