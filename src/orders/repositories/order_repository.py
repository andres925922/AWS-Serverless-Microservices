from common.infrastructure.repositories import DynamoCommonRepository

class OrderRepository(DynamoCommonRepository):
    def __init__(self):
        super().__init__('orders')