import json
from pathlib import Path

from pydantic import BaseModel

NATIVE_ETH_ADDRESS = "0x0000000000000000000000000000000000000000"
ABI_DIR = Path(__file__).parents[1] / "abi"

def get_abi(name: str) -> str:
    with open(ABI_DIR / f"{name}.json") as fin:
        return json.dumps(json.load(fin))


class Chain(BaseModel):
    chain_id: int
    rpc: str
    scan: str
    code: int
