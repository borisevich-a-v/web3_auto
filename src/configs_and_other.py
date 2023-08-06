from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings

from src.constants import Tokens


class Chain(BaseModel):
    chain_id: int
    rpc: HttpUrl
    scan: HttpUrl
    token: Tokens
    code: int


ERA = Chain(
    chain_id=324,
    rpc="https://zksync-era.blockpi.network/v1/rpc/public",
    scan="https://explorer.zksync.io/tx",
    token=Tokens.ETH,
    code=9014,
)

ARB = Chain(
    chain_id=42161,
    rpc="https://endpoints.omniatech.io/v1/arbitrum/one/public",
    scan="https://arbiscan.io/tx",
    token=Tokens.ETH,
    code=9002,
)


class Settings(BaseSettings):
    private_key: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
