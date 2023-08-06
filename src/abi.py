import json


def get_abi(name) -> str:
    with open(f"../abi/{name}.json") as fin:
        return json.dumps(json.load(fin))


class ABI:
    SYNCSWAP_CLASSIC_POOL_FACTORY = get_abi("syncswap_classic_pool_factory")
    ERC20 = get_abi("erc20")
    SYNCSWAP_ROUTER = get_abi("syncswap_router")
