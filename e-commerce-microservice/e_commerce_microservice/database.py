from aws_cdk import RemovalPolicy
from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode, Table

from constructs import Construct

class DatabaseStack(Construct):
    """
    This class contains all DynamoDB tables for the e-commerce microservice definitions
    and their creation.

    Attributes:
        products_table (Table): The DynamoDB table for products.
        orders_table (Table): The DynamoDB table for orders.
        basket_table (Table): The DynamoDB table for baskets.
    
    Methods:
        create_tables(): Creates all the DynamoDB tables.
        
    """

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    def create_tables(self) -> "DatabaseStack":
        """
           Builder method to create all DynamoDB tables for the e-commerce microservice. 
        """
        self._create_products_table()
        self._create_basket_table()
        self._create_orders_table()
        return self


    def _create_products_table(self):
        """
        Create the products table in DynamoDB.
        """
        # DynamoDB table for products
        self.products_table = Table(
            self, "products",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            # sort_key=Attribute(name="created_at", type=AttributeType.STRING),
            table_name="products",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # NOT recommended for production code
        )

    def _create_basket_table(self):
        """
        Create the basket table in DynamoDB.
        """
        # DynamoDB table for baskets
        self.basket_table = Table(
            self, "basket",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            # sort_key=Attribute(name="created_at", type=AttributeType.STRING),
            table_name="basket",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # NOT recommended for production code
        )

    def _create_orders_table(self):
        """
        Create the orders table in DynamoDB.
        """
        # DynamoDB table for orders
        self.orders_table = Table(
            self, "orders",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            # sort_key=Attribute(name="created_at", type=AttributeType.STRING),
            table_name="orders",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # NOT recommended for production code
        )