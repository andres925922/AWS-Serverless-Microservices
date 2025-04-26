from abc import ABC
from aws_cdk import Duration
from aws_cdk.aws_lambda import Function, FunctionAttributes, Runtime, Code
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
        self.props: IMicroserviceProps = props
        self.products_lambda: Function = self._create_products_lambda_microservice()

    def _create_products_lambda_microservice(self) -> Function:
        products_lambda = Function(
            self, "ProductsLambda",
            runtime=Runtime.PYTHON_3_12,
            handler="products_lambda.handler",
            code=Code.from_asset("../src/products"),  # relative to cdk.json
            environment={
                "PRIMARY_KEY": "id",
                "PRODUCTS_TABLE": self.props.products_table.table_name,
            },
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        self.props.products_table.grant_read_write_data(products_lambda)

        return products_lambda