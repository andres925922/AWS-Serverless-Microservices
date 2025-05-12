from common.infrastructure.repositories import DynamoCommonRepository

class BasketRepository(DynamoCommonRepository):
    def __init__(self):
        super().__init__('basket')