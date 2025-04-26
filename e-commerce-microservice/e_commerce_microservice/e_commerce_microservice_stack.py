from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)
from constructs import Construct

from database import DatabaseStack

class ECommerceMicroserviceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # DynmamoDB tables
        database: DatabaseStack = DatabaseStack(self, "DatabaseStack").create_tables()
