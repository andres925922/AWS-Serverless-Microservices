from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
)
from constructs import Construct

class HelloCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        queue = sqs.Queue(
            self, "HelloCdkQueue",
            visibility_timeout=Duration.seconds(300),
            fifo=True,
        )

        bucket = s3.Bucket(
            self, "HelloCdkBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
