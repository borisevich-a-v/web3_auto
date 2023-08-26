from datetime import datetime

from activities import app_to_activities_map
from applications import Applications
from configs import settings
from eth_typing import HexStr
from models import Tx, TxDB
from repositories.transactions import TxRepository

from crypto.chains import era
from crypto.chains.era import Tokens


def get_private_key_for_acc(public_key: HexStr) -> str:  # TODO get it from AWS
    return settings.private_key


class Executor:
    def __init__(self, public_key, rnd, tx_repository: TxRepository) -> None:
        self.public_key = public_key
        self.private_key = get_private_key_for_acc(self.public_key)
        self.rnd = rnd
        self.tx_repository = tx_repository

    def perform_activity(self) -> None:
        tx = self._calculate_next_transaction()
        swap_class = app_to_activities_map[tx.application]
        tx_hash = swap_class(
            private_key=self.private_key,
            from_token=tx.from_token,
            to_token=tx.to_token,
            amount_to_swap=tx.amount,
            rnd=self.rnd,
        ).swap()
        self._save_tx(tx, tx_hash)

    def _calculate_next_transaction(self) -> Tx:  # TODO: refactor it
        token_from, token_to = self._get_swap_pair()
        tx = Tx(
            chain=era.chain.name,
            application=Applications.SYNCSWAP,
            from_token=token_from,
            to_token=token_to,
            amount=self._get_amount(token_from),
        )
        print(f"Next transaction is {tx}")
        return tx

    def _get_swap_pair(self):
        return Tokens.USDC, Tokens.ETH

    def _get_amount(self, token) -> int:
        if token is Tokens.USDC:
            return 0.5 * 10**6

    def _save_tx(self, tx, tx_hash) -> None:
        print("Tx was performed", tx)
        tx_db = TxDB(
            hash=tx_hash,
            chain=tx.chain,
            account_public_key=self.public_key,
            app=str(tx.application),  # TODO make enum
            amount_in_usd=0,  # TODO calculate later
            amount=tx.amount,
            from_token=tx.from_token,
            to_token=tx.to_token,
            tx_date=datetime.now(),
        )
        self.tx_repository.post_tx(tx_db)

    def __repr__(self):
        return f"Account(public_key={self.public_key})"
