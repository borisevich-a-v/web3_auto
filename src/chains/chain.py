import json

from pydantic import BaseModel

NATIVE_ETH_ADDRESS = "0x0000000000000000000000000000000000000000"


def get_abi(name: str) -> str:
    with open(f"assets/abi/{name}.json") as fin:
        return json.dumps(json.load(fin))


class Chain(BaseModel):
    chain_id: int
    rpc: str
    scan: str
    code: int
