from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct

class ApigateLambdaSyncStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        helloLambda = lambda_.Function(
            self, "HelloLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="hello_handler.main",
            code=lambda_.Code.from_asset("../lambdas/hello")
        )

        helloLambdaApi = apigateway.LambdaRestApi(
            self, "HelloLambdaApiGateway",
            handler=helloLambda,
            proxy=True
        )
