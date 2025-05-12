from abc import ABC
from aws_cdk import Duration, BundlingOptions, DockerImage
from aws_cdk.aws_lambda import Function, FunctionAttributes, Runtime, Code, LayerVersion
from aws_cdk.aws_dynamodb import  ITable

from constructs import Construct

class IMicroserviceProps(ABC):
    products_table: ITable|None
    orders_table: ITable|None
    basket_table: ITable|None

class MicroserviceProps(IMicroserviceProps):
    def __init__(self, 
                 products_table: ITable = None, 
                 orders_table: ITable = None, 
                 basket_table: ITable = None
    ):
        self.products_table = products_table
        self.orders_table = orders_table
        self.basket_table = basket_table

class LambdaStack(Construct):

    def __init__(self, scope: Construct, id: str, props: IMicroserviceProps, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._props: IMicroserviceProps = props
        self._common_layer: LayerVersion = self._create_dependencies_layer()
        self.products_lambda: Function = self._create_products_lambda_microservice()
        self.basket_lambda: Function = self._create_basket_lambda_microservice()
        self.orders_lambda: Function = self._create_orders_lambda_microservice()

    def _create_products_lambda_microservice(self) -> Function:
        products_lambda = Function(
            self, "ProductsLambda",
            runtime=Runtime.PYTHON_3_12,
            handler="handler.handle",
            code=Code.from_asset("../src/products"),  # relative to cdk.json
            layers=[
                self._common_layer,
            ], 
            environment={
                "PRIMARY_KEY": "id",
                "PRODUCTS_TABLE": self._props.products_table.table_name,
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.products_table.grant_read_write_data(products_lambda)

        return products_lambda
    
    def _create_basket_lambda_microservice(self) -> Function:
        basket_lambda = Function(
            self, "BasketLambda",
            runtime=Runtime.PYTHON_3_12,
            handler="handler.handle",
            code=Code.from_asset("../src/basket"),  # relative to cdk.json
            layers=[
                self._common_layer,
            ], 
            environment={
                "PRIMARY_KEY": "id",
                "BASKET_TABLE": self._props.basket_table.table_name,
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.basket_table.grant_read_write_data(basket_lambda)

        return basket_lambda
    
    def _create_orders_lambda_microservice(self) -> Function:
        orders_lambda = Function(
            self, "OrdersLambda",
            runtime=Runtime.PYTHON_3_12,
            handler="handler.handle",
            code=Code.from_asset("../src/orders"),  # relative to cdk.json
            layers=[
                self._common_layer,
            ], 
            environment={
                "PRIMARY_KEY": "id",
                "ORDERS_TABLE": self._props.orders_table.table_name,
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.basket_table.grant_read_write_data(orders_lambda)

        return orders_lambda

    def _create_dependencies_layer(self) -> LayerVersion:
        return LayerVersion(
            self, "DependenciesLayer",
            code=Code.from_asset(
                path="../src/_layers/dependencies",  # where your requirements.txt is
                bundling=BundlingOptions(
                    image=DockerImage.from_registry("python:3.12-slim"), 
                    command=[
                        "bash", "-c",
                        "pip install --no-cache-dir -r requirements.txt -t /asset-output/python && cp -r python/* /asset-output/python/ "
                    ],
                ),
            ),
            compatible_runtimes=[Runtime.PYTHON_3_12],
            description="Python libraries like boto3, requests, etc."
        )
