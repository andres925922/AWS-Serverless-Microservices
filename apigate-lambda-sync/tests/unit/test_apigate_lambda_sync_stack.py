import aws_cdk as core
import aws_cdk.assertions as assertions

from apigate_lambda_sync.apigate_lambda_sync_stack import ApigateLambdaSyncStack

# example tests. To run these tests, uncomment this file along with the example
# resource in apigate_lambda_sync/apigate_lambda_sync_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApigateLambdaSyncStack(app, "apigate-lambda-sync")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
