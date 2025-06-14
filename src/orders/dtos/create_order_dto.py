from dataclasses import dataclass

@dataclass
class CreateOrderDto:
    userId: str
    items: list[dict]
    totalPrice: float
