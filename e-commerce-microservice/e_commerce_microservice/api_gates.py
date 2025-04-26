from abc import ABC
from aws_cdk.aws_apigateway import LambdaRestApi
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


    def _create_products_api(self, products_lambda: IFunction) -> None:

        # Create the API Gateway
        self.api = LambdaRestApi(
            self, "ProductsApi",
            handler=products_lambda,
            proxy=False,
            rest_api_name="Products Service",
            description="This service serves products.",
        )

        # Define the /products resource
        products_resource = self.api.root.add_resource("products")
        products_resource.add_method("GET")  # GET /products
        products_resource.add_method("POST")  # POST /products
        products_resource.add_method("OPTIONS")

        # Define the /products/{id} resource
        single_product_resource = products_resource.add_resource("{id}")
        single_product_resource.add_method("GET")
        single_product_resource.add_method("PUT")
        single_product_resource.add_method("DELETE")
        single_product_resource.add_method("OPTIONS")