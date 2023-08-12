from src.chains import era
from src.configs import settings
from src.syncswap import SyncswapSwap

swap = SyncswapSwap(
    private_key=settings.private_key, from_token=era.Tokens.USDC, to_token=era.Tokens.ZZ, amount_to_swap=0.5 * 10**6
)

print(swap.swap())
