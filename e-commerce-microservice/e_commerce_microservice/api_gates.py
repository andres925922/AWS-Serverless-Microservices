from abc import ABC
from aws_cdk.aws_apigateway import LambdaRestApi, LambdaIntegration, Model, RequestValidator, JsonSchema, JsonSchemaType
from aws_cdk.aws_lambda import IFunction

from constructs import Construct

class IApiGatewayProps(ABC):
    products_lambda: IFunction|None
    orders_lambda: IFunction|None
    basket_lambda: IFunction|None

class ApiGatewayProps(IApiGatewayProps):
    def __init__(self, 
                 *,
                 products_lambda: IFunction = None, 
                 orders_lambda: IFunction = None, 
                 basket_lambda: IFunction = None
    ):
        self.products_lambda = products_lambda
        self.orders_lambda = orders_lambda
        self.basket_lambda = basket_lambda

class ApiGatewayStack(Construct):
    def __init__(self, scope: Construct, id: str, props: IApiGatewayProps, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.props: IApiGatewayProps = props

        self._create_products_api(self.props.products_lambda)
        self._create_basket_api(self.props.basket_lambda)
        self._create_orders_api(self.props.orders_lambda)


    def _create_products_api(self, products_lambda: IFunction) -> None:

        # Create the API Gateway
        self.products_api = LambdaRestApi(
            self, "ProductsApi",
            handler=products_lambda,
            proxy=False,
            rest_api_name="Products Service",
            description="This service serves products.",
        )

        # Define the request model for the API
        post_products_model = Model(
            self, "PostProductsModel",
            rest_api=self.products_api,
            content_type="application/json",
            model_name="PostProductsModel",
            schema=JsonSchema(
                type=JsonSchemaType.OBJECT,
                properties={
                    "name": JsonSchema(type=JsonSchemaType.STRING),
                    "category": JsonSchema(type=JsonSchemaType.STRING),
                    "price": JsonSchema(type=JsonSchemaType.NUMBER),
                    "description": JsonSchema(type=JsonSchemaType.STRING),
                    "created_at": JsonSchema(type=JsonSchemaType.STRING),
                },
                required=["name", "price"],
            ),
        )
        post_products_validator = RequestValidator(
            self, "PostProductsValidator",
            rest_api=self.products_api,
            request_validator_name="PostProductsValidator",
            validate_request_body=True,
            validate_request_parameters=False,
        )

        products_integration = LambdaIntegration(products_lambda)

        # Define the /products resource
        products_resource = self.products_api.root.add_resource("products", default_integration=products_integration)
        products_resource.add_method("GET")  # GET /products
        products_resource.add_method(
            "POST", 
            request_validator=post_products_validator, 
            request_models={"application/json": post_products_model}
        )  # POST /products
        products_resource.add_method("OPTIONS")

        # Define the /products/{id} resource
        single_product_resource = products_resource.add_resource("{id}")
        single_product_resource.add_method("GET", products_integration)
        single_product_resource.add_method("PUT", products_integration)
        single_product_resource.add_method("DELETE", products_integration)
        single_product_resource.add_method("OPTIONS")


    def _create_basket_api(self, basket_lambda: IFunction) -> None:
                # Create the API Gateway
        self.basket_api = LambdaRestApi(
            self, "BasketApi",
            handler=basket_lambda,
            proxy=False,
            rest_api_name="Basket Service",
            description="This service serves basket.",
        )

        basket_integration = LambdaIntegration(basket_lambda)

        # Basket API
        basket_resource = self.basket_api.root.add_resource("basket", default_integration=basket_integration)
        basket_resource.add_method("GET")

        # Define the /basket/{id} resource
        single_basket_resource = basket_resource.add_resource("{id}")
        single_basket_resource.add_method("GET", basket_integration)



    def _create_orders_api(self, orders_lambda: IFunction) -> None:
                # Create the API Gateway
        self.orders_api = LambdaRestApi(
            self, "OrdersApi",
            handler=orders_lambda,
            proxy=False,
            rest_api_name="Orders Service",
            description="This service serves orders.",
        )

        orders_integration = LambdaIntegration(orders_lambda)

        # Basket API
        orders_resource = self.orders_api.root.add_resource("orders", default_integration=orders_integration)
        orders_resource.add_method("GET")

        # Define the /orders/{id} resource
        single_orders_resource = orders_resource.add_resource("{id}")
        single_orders_resource.add_method("GET", orders_integration)