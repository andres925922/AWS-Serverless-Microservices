from aws_cdk import Stack, Duration
from constructs import Construct

from .databases import DatabaseStack
from .microservices import MicroserviceProps, LambdaStack
from .api_gates import ApiGatewayStack, ApiGatewayProps
from .event_bus import EventBusFactory
from .sqs_queue import SQSQueueFactory, SQSQueueProps

class ECommerceMicroserviceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        database: DatabaseStack = DatabaseStack(self, "DatabaseStack").create_tables()

        # Lambda functions
        microservice_props = MicroserviceProps(
            products_table=database.products_table,
            basket_table=database.basket_table,
            orders_table=database.orders_table
        )
        lambda_stack: LambdaStack = LambdaStack(self, "LambdaStack", props=microservice_props)

        # API Gateway
        api_gateway_props = ApiGatewayProps(
            products_lambda=lambda_stack.products_lambda,
            basket_lambda=lambda_stack.basket_lambda,
            orders_lambda=lambda_stack.orders_lambda
        )
        api_gateway_stack: ApiGatewayStack = ApiGatewayStack(self, "ApiGatewayStack", props=api_gateway_props)

        e_commerce_event_bus = EventBusFactory(self, "ECommerceEventBus").create_event_bus("e-commerce-event-bus")

        order_queue = SQSQueueFactory(self, 
                                    "OrderQueue", 
                                    props=SQSQueueProps("e-commerce-sqs-queue", 
                                        visibility_timeout=Duration.seconds(30),
                                        consumer=lambda_stack.orders_lambda
                                    )
                                ) \
                                .create_queue() \
                                .add_consumer()
        
        # TODO: attach rule can receive a property object instead of multiple parameters
        e_commerce_event_bus.attach_rule(
                rule_id="CheckoutBasketRule",
                desc="Rule for order created events",
                souces=["com.e_commerce.checkout_basket"],
                detail_types=["checkout_basket"]) \
            .add_sqs_target("CheckoutBasketRule", order_queue) \
            .grant_publish_permissions(lambda_stack.basket_lambda)
