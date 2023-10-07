import logging
from datetime import datetime

from activities import Activities
from eth_typing import HexStr
from infrastructure.repositories.transactions import TxRepository
from models import Tx, TxDB

from crypto.chains import era
from crypto.chains.era import Tokens

logger = logging.getLogger()


class Executor:
    def __init__(self, public_key, rnd, tx_repository: TxRepository, secret_manager: ...) -> None:
        self.rnd = rnd
        self._tx_repository = tx_repository
        self._secret_manager = secret_manager

        self.public_key = public_key
        self.private_key = self.get_private_key_for_acc(self.public_key)

    def get_private_key_for_acc(self, public_key: HexStr) -> str:  # TODO implement repository
        logger.info("Retrieve private key for %s", public_key)
        return self._secret_manager.get_secret_value(SecretId=public_key)[public_key]

    def perform_activity(self) -> None:
        tx = self._calculate_next_transaction()
        swap_class = app_to_activities_map[tx.application]
        swap = swap_class(
            private_key=self.private_key,
            from_token=tx.from_token,
            to_token=tx.to_token,
            amount_to_swap=tx.amount,
            rnd=self.rnd,
        )
        logger.info(swap)
        tx_hash = swap.swap()
        self._save_tx(tx, tx_hash)

    def _calculate_next_transaction(self) -> Tx:  # TODO: refactor it
        token_from, token_to = self._get_swap_pair()
        tx = Tx(
            chain=era.chain.name,
            application=Activities.SYNCSWAP,
            from_token=token_from,
            to_token=token_to,
            amount=self._get_amount(token_from),
        )
        print(f"Next transaction is {tx}")
        return tx

    def _get_swap_pair(self):
        return Tokens.USDT, Tokens.ETH

    def _get_amount(self, token) -> int:
        if token in [Tokens.USDC, Tokens.USDT]:
            return 0.5 * 10**6

    def _save_tx(self, tx, tx_hash) -> None:
        logger.info("Saving tx for %s", self.public_key)
        tx_db = TxDB(
            hash=tx_hash,
            chain=tx.chain,
            account_public_key=self.public_key,
            app=str(tx.application),  # TODO make enum
            amount_in_usd=0,  # TODO calculate later
            amount=tx.amount,
            from_token=tx.from_token.value,
            to_token=tx.to_token.value,
            tx_date=datetime.now(),
        )
        self._tx_repository.post_tx(tx_db)

    def __repr__(self):
        return f"Account(public_key={self.public_key})"
