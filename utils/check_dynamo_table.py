import boto3

from configs import settings
from infrastructure.dynamodb import create_dynamodb_resource
from infrastructure.repositories.transactions import TxRepository

aws_session = boto3.session.Session()
dynamodb = create_dynamodb_resource(aws_session, True)
tx_repository = TxRepository(dynamodb)

txs = tx_repository.get_account_txs(settings.local_public_key)
for t in txs:
    print(t)
