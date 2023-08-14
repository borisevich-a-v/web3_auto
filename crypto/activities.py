from enum import Enum

from db import Applications

from crypto.swaps import Swap
from crypto.syncswap import SyncswapSwap


class Activities(Enum):
    SYNCSWAP: Swap = SyncswapSwap


app_to_activities_map = {Applications.SYNCSWAP: Activities.SYNCSWAP.value}
