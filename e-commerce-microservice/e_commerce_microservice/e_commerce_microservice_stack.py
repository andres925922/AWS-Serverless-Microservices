from aws_cdk import Stack
from constructs import Construct

from .databases import DatabaseStack
from .microservices import MicroserviceProps, LambdaStack
from .api_gates import ApiGatewayStack, ApiGatewayProps
from .event_bus import EventBusFactory

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
        e_commerce_event_bus.attach_rule(
                rule_id="CheckoutBasketRule",
                desc="Rule for order created events",
                souces=["com.e_commerce.checkout_basket"],
                detail_types=["checkout_basket"]) \
            .add_target("CheckoutBasketRule", lambda_stack.orders_lambda) \
            .grant_publish_permissions(lambda_stack.basket_lambda)
