import random

from web3 import Web3

from src.configs_and_other import ERA, Tokens


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
        self.web3 = Web3(Web3.HTTPProvider(ERA.rpc))
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    async def swap(self) -> None:
        ...

    def get_balance(self, token: Tokens) -> float:
        balance = self.web3.eth.get_balance(self.address_wallet)
        return balance

    def send_eth(self, private_key):
        txn = {
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            "from": self.address_wallet,
            "to": self.address_wallet,
            "value": self.web3.to_wei(0.0005, "ether"),
            "gas": 2_000_000,
            "gasPrice": self.web3.eth.gas_price,
            "chainId": ERA.chain_id,
        }
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key)
        print("sending tx...")
        txn_response = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_response
