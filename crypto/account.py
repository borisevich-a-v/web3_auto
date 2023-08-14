from activities import app_to_activities_map
from configs import settings
from db import Applications, Tx

from crypto.chains import era


class Account:
    def __init__(self, public_key, rnd) -> None:
        self.public_key = public_key
        self.id = "0"
        self.private_key = self.get_private_key_for_acc()
        self.rnd = rnd

    def _calculate_next_transaction(self) -> Tx:
        tx = Tx(
            id_="0",
            account_id=self.id,
            application=Applications.SYNCSWAP,
            amount_in_usd=0.7,
            from_=era.Tokens.ZZ,
            to_=era.Tokens.USDC,
        )
        return tx

    def get_private_key_for_acc(self) -> str:
        return settings.private_key

    def _perform_activity(self) -> None:
        tx = self._calculate_next_transaction()
        swap_class = app_to_activities_map[tx.application]
        swap_class(
            private_key=self.private_key,
            from_token=tx.from_,
            to_token=tx.to_,
            amount_to_swap=self.convert_usd_to_token(tx.amount_in_usd, tx.from_),
            rnd=self.rnd,
        ).swap()
        self.save_tx(tx)

    def save_tx(self, tx):
        print(tx)

    def convert_usd_to_token(self, usd_amount, token) -> int:
        return usd_amount * 8.11 * 10**18
