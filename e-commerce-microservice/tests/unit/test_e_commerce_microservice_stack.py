import aws_cdk as core
import aws_cdk.assertions as assertions

from e_commerce_microservice.e_commerce_microservice_stack import ECommerceMicroserviceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in e_commerce_microservice/e_commerce_microservice_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ECommerceMicroserviceStack(app, "e-commerce-microservice")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
