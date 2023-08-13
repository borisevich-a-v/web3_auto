from crypto.configs import RandomConfig
from crypto.crypto.chains import era
from crypto.crypto.swap_factory import SwapFactory
from crypto.crypto.syncswap import SyncswapSwap


class SyncswapFactory(SwapFactory):
    rnd = RandomConfig()

    @classmethod
    def get_syncswap_swap(
        cls, private_key: str, from_token: era.Tokens, to_token: era.Tokens, amount_to_swap: float
    ) -> SyncswapSwap:
        SyncswapSwap(
            private_key=private_key,
            from_token=from_token,
            to_token=to_token,
            amount_to_swap=amount_to_swap,
            rnd=cls.rnd,
        )
