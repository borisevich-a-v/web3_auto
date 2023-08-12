from enum import StrEnum

from .chain import NATIVE_ETH_ADDRESS, Chain, get_abi


class Tokens(StrEnum):
    NATIVE = NATIVE_ETH_ADDRESS
    ETH = "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91"
    USDC = "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"
    USDT = "0x493257fd37edb34451f62edf8d2a0c418852ba4c"
    WBTC = "0xbbeb516fb02a01611cbbe0453fe3c580d7281011"


chain = Chain(
    chain_id=324,
    rpc="https://zksync-era.blockpi.network/v1/rpc/public",
    scan="https://explorer.zksync.io/tx",
    code=9014,
)


class ABI:
    SYNCSWAP_CLASSIC_POOL_FACTORY: str = get_abi("syncswap_classic_pool_factory")
    ERC20: str = get_abi("erc20")
    SYNCSWAP_ROUTER: str = get_abi("syncswap_router")
