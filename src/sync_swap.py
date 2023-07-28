import random

from web3 import Web3

from src.configs_and_other import ARB, ERA, Tokens


class SyncSwapConfig:
    from_token = "ETH"
    to_token = "USDC"
    amount_from = 0.004
    amount_to = 0.004


class SyncswapSwap:
    def __init__(
        self, private_key: str, from_token: Tokens, to_token: Tokens, amount_from: float, amount_up_to: float
    ) -> None:
        self.private_key = private_key
        self.from_token = from_token
        self.amount_to_swap = random.uniform(amount_from, amount_up_to)

        self.classic_pool_factory_address = ...
        self.router_address = ...
        self.web3 = Web3(Web3.HTTPProvider(ARB.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def swap(self) -> None:
        ...

    def get_balance(self, token: Tokens) -> float:
        return self.web3.eth.get_balance(self.address_wallet) / 10**18
