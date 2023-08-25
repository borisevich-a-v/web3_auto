import boto3
from configs import settings
from repositories.account import AccountRepository
from runner import Runner

dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_key,
)
account_repository = AccountRepository(dynamodb)

runner = Runner(account_repository=account_repository)
runner.run()
