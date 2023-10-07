from web3 import Web3

from configs import settings
from crypto_lib.chains import era
from crypto_lib.syncswap import SyncswapSwap
from crypto_lib.web3_utils import get_balance

web3 = Web3(Web3.HTTPProvider(era.chain.rpc))


def main():
    token_from = era.Tokens.USDT
    token_to = era.Tokens.ETH
    amount = get_balance(web3, settings.local_public_key, token_from)
    print(amount)
    if amount == 0:
        exit()

    swap = SyncswapSwap(settings.local_private_key, token_from, token_to, amount)
    print(swap.swap())


main()
