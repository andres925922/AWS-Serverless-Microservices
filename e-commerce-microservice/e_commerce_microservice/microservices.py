from abc import ABC
from aws_cdk import Duration
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
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
        self.products_lambda: DockerImageFunction = self._create_products_lambda_microservice()
        self.basket_lambda: DockerImageFunction = self._create_basket_lambda_microservice()
        self.orders_lambda: DockerImageFunction = self._create_orders_lambda_microservice()

    def _create_products_lambda_microservice(self) -> DockerImageFunction:
        products_lambda = DockerImageFunction(
            self, "ProductsLambda",
            code=DockerImageCode.from_image_asset(
                directory="../src",
                file="Dockerfile",
                build_args={
                    "LAMBDA_ROOT_SOURCE": "products"
                }
            ),
            environment={
                "PRIMARY_KEY": "id",
                "PRODUCTS_TABLE": self._props.products_table.table_name,
                "LAMBDA_HANDLER": "products.handler.handle",
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.products_table.grant_read_write_data(products_lambda)

        return products_lambda
    
    def _create_basket_lambda_microservice(self) -> DockerImageFunction:
        basket_lambda = DockerImageFunction(
            self, "BasketLambda",
            code=DockerImageCode.from_image_asset(
                directory="../src",
                file="Dockerfile",
                build_args={
                    "LAMBDA_ROOT_SOURCE": "basket"
                }
            ),
            environment={
                "PRIMARY_KEY": "id",
                "BASKET_TABLE": self._props.basket_table.table_name,
                "LAMBDA_HANDLER": "basket.handler.handle",
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.basket_table.grant_read_write_data(basket_lambda)

        return basket_lambda
    
    def _create_orders_lambda_microservice(self) -> DockerImageFunction:
        orders_lambda = DockerImageFunction(
            self, "OrdersLambda",
            code=DockerImageCode.from_image_asset(
                directory="../src",
                file="Dockerfile",
                build_args={
                    "LAMBDA_ROOT_SOURCE": "orders"
                }
            ),
            environment={
                "PRIMARY_KEY": "id",
                "ORDERS_TABLE": self._props.orders_table.table_name,
                "LAMBDA_HANDLER": "orders.handler.handle",
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self._props.orders_table.grant_read_write_data(orders_lambda)

        return orders_lambda
