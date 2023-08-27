import logging
import os

import boto3
from activities import Activities
from configs import RandomConfig, settings
from infrastructure.repositories.account import AccountRepository
from infrastructure.repositories.transactions import TxRepository
from infrastructure.secret_manager_stub import SecretManagerStub
from logger import configure_logging
from runner import Runner

configure_logging()
logger = logging.getLogger()

aws_session = boto3.session.Session()
dynamodb = aws_session.resource(
    "dynamodb",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_key,
    endpoint_url=settings.aws_endpoint_url,
)

if os.getenv("ENVIRONMENT") == "local":  # TODO
    logger.info("Local for secret management")
    secret_manager = SecretManagerStub(settings.local_public_key, settings.local_private_key)
else:
    secret_manager = aws_session.client(
        "secretsmanager",
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=settings.aws_region,
    )

account_repository = AccountRepository(dynamodb)
tx_repository = TxRepository(dynamodb)

runner = Runner(
    account_repository=account_repository,
    tx_repository=tx_repository,
    secret_manager=secret_manager,
    random_config=RandomConfig(),
    activities=Activities,
)
runner.run()
