from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    local_public_key: Optional[str]
    local_private_key: Optional[str]


settings = Settings(_env_file="../.env", _env_file_encoding="utf-8")
