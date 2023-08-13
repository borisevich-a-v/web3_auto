from crypto.crypto.chains import era
from crypto.crypto.syncswap import SyncswapSwap

from .configs import Activities, RandomConfig, Settings
from .runner import Runner

settings = Settings(_env_file=".env", _env_file_encoding="utf-8")


db = initdatabase(settings)
queue = initqueue(settings.worker_queue_name)

rnd = RandomConfig()

swap = SyncswapSwap(
    private_key=settings.private_key,
    from_token=era.Tokens.USDC,
    to_token=era.Tokens.ZZ,
    amount_to_swap=0.5 * 10**6,
    rnd=rnd,
)

accounts = Runner(db=db, queue=queue, rnd=rnd, activities=Activities)
