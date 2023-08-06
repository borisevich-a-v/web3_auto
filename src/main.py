from src.configs_and_other import settings
from src.constants import Tokens
from src.syncswap import SyncswapSwap

swap = SyncswapSwap(
    private_key=settings.private_key, from_token=Tokens.USDC, to_token=Tokens.USDT, amount_to_swap=1 * 10**6
)

print(swap.swap())
