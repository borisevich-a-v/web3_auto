import logging
import random
import time
import traceback
from typing import Any

from eth_abi import encode
from eth_typing import HexStr
from web3 import Web3
from web3.types import SignedTx

from .chains import era
from .errors import NoPoolError, NotEnoughBalanceError
from .swaps import BaseSwap
from .web3_utils import get_balance

logger = logging.getLogger()


class SyncswapSwap(BaseSwap):
    CLASSIC_POOL_FACTORY_ADDRESS = "0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb"
    ROUTER_ADDRESS = "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295"

    DEX = "syncswap"

    def __init__(self, private_key: str, from_token: era.Tokens, to_token: era.Tokens, amount_to_swap: float) -> None:
        self.from_token = from_token

        self.from_token_adr = Web3.to_checksum_address(self.from_token.value)
        self.to_token = to_token
        self.to_token_adr = Web3.to_checksum_address(self.to_token.value)
        self.amount_to_swap = int(amount_to_swap)

        self.web3 = Web3(Web3.HTTPProvider(era.chain.rpc))
        self.account = self.web3.eth.account.from_key(private_key)

    def swap(self) -> HexStr:
        print(f"Swapping {self.from_token} to {self.to_token}")
        self._validate_amount_to_swap()
        paths = self._get_paths(self.amount_to_swap)
        print("Paths was found")
        if self.from_token is not era.Tokens.ETH:
            try:
                self.approve_token(self.amount_to_swap)
            except Exception:
                traceback.print_exc()
            print("Required amount approved")
        tx_hash = self._send_transaction(paths)
        return tx_hash

    def approve_token(self, amount: float) -> None:  # TODO refactoring
        amount_to_approve = amount or self.amount_to_swap
        spender = self.web3.to_checksum_address(self.ROUTER_ADDRESS)
        contract = self.web3.eth.contract(address=self.from_token_adr, abi=era.ABI.ERC20)
        allowance_amount = contract.functions.allowance(self.account.address, spender).call()

        if allowance_amount > amount_to_approve:
            return

        gas_price = self.web3.eth.gas_price
        gas_price = int(gas_price * random.uniform(1.01, 1.05))

        value_to_approve = amount_to_approve  # random.choices([amount_to_approve, get_random_value_occur_same_number(length_range=(40, 55))], weights=(4, 1))[0]
        print(f"Give approve for {value_to_approve}")
        tx = contract.functions.approve(spender, value_to_approve).build_transaction(
            {
                "chainId": self.web3.eth.chain_id,
                "from": self.account.address,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
                "gasPrice": gas_price,
                "gas": 0,
                "value": 0,
            }
        )

        gas_limit = self.web3.eth.estimate_gas(tx)
        tx["gas"] = gas_limit
        signed_tx = self.account.sign_transaction(tx)
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(raw_tx_hash)

        while tx_receipt is None:
            time.sleep(1)
            tx_receipt = self.web3.eth.get_transaction_receipt(raw_tx_hash)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        print(f"Token approved | Tx hash: {tx_hash}")
        time.sleep(random.randint(5, 120))

    def _send_transaction(self, paths: list[dict[str, Any]]) -> HexStr:
        signed_tx = self._get_signed_tx(paths, self.amount_to_swap)
        raw_tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        return tx_hash

    def _get_signed_tx(self, paths: list[dict[str, Any]], value: float) -> SignedTx:
        router = self.web3.eth.contract(
            address=Web3.to_checksum_address(self.ROUTER_ADDRESS), abi=era.ABI.SYNCSWAP_ROUTER
        )
        tx = router.functions.swap(paths, 0, int(self.web3.eth.get_block("latest").timestamp) + 1200).build_transaction(
            {
                "from": self.account.address,
                "value": value if self.from_token.value.lower() == "eth" else 0,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
                "maxFeePerGas": 0,
                "maxPriorityFeePerGas": 0,
                "gas": 0,
            }
        )
        tx.update({"maxFeePerGas": self.web3.eth.gas_price})
        tx.update({"maxPriorityFeePerGas": self.web3.eth.gas_price})
        gas_limit = self.web3.eth.estimate_gas(tx)
        tx.update({"gas": gas_limit})
        signed_tx = self.account.sign_transaction(tx)
        return signed_tx

    def _validate_amount_to_swap(self) -> None:
        balance = self.get_balance(self.from_token)
        if balance < self.amount_to_swap:
            raise NotEnoughBalanceError(
                f"Current balance={balance} of wallet {self.account.address} "
                f"is less then required amount to swap={self.amount_to_swap}"
            )
        print("Enough balance for swap")

    def _get_paths(self, value: float) -> list[dict[str, Any]]:
        pool_address = self._get_pool_address()
        swap_data = encode(["address", "address", "uint8"], [self.from_token_adr, self.account.address, 1])
        steps = [{"pool": pool_address, "data": swap_data, "callback": era.Tokens.NATIVE.value, "callbackData": "0x"}]
        paths = [
            {
                "steps": steps,
                "tokenIn": Web3.to_checksum_address(era.Tokens.NATIVE.value)
                if self.from_token is era.Tokens.ETH
                else self.from_token_adr,
                "amountIn": value,
            }
        ]
        return paths

    def _get_pool_address(self) -> str:
        classic_pool_factory = self.web3.eth.contract(
            address=Web3.to_checksum_address(self.CLASSIC_POOL_FACTORY_ADDRESS),
            abi=era.ABI.SYNCSWAP_CLASSIC_POOL_FACTORY,
        )
        pool_address = classic_pool_factory.functions.getPool(self.from_token_adr, self.to_token_adr).call()

        if pool_address == "0x0000000000000000000000000000000000000000":
            raise NoPoolError("Yep")

        return str(pool_address)

    def get_balance(self, token: era.Tokens) -> float:
        return get_balance(self.web3, self.account.address, token)
