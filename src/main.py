from src.configs_and_other import Tokens, settings
from src.sync_swap import SyncswapSwap

swap = SyncswapSwap(
    private_key=settings.private_key, from_token=Tokens.ETH, to_token=Tokens.USDC, amount_from=0, amount_up_to=0.00001
)

print(swap.send_eth(settings.private_key))
