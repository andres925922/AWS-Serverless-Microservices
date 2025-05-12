from common.infrastructure.repositories import DynamoCommonRepository

class ProductRepository(DynamoCommonRepository):
    def __init__(self):
        super().__init__('products')