from src.chains import era
from src.configs import settings
from src.syncswap import SyncswapSwap

swap = SyncswapSwap(
    private_key=settings.private_key, from_token=era.Tokens.USDC, to_token=era.Tokens.USDT, amount_to_swap=1 * 10**6
)

print(swap.swap())
