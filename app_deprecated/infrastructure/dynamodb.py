import os

from boto3 import Session
from configs import settings


def create_dynamodb_resource(aws_session: Session, force_local=False):
    print(settings)
    dynamodb_args = {
        "service_name": "dynamodb",
        "region_name": settings.aws_region,
        "aws_access_key_id": settings.aws_access_key,
        "aws_secret_access_key": settings.aws_secret_key,
    }
    if force_local or os.getenv("ENVIRONMENT") == "local":
        if not settings.aws_endpoint_url:
            raise ValueError("If you want to use local db, the you shall define local url")
        dynamodb_args.update({"endpoint_url": settings.aws_endpoint_url})

    return aws_session.resource(**dynamodb_args)
