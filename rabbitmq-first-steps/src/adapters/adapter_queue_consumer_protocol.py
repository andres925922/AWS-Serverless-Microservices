from typing import Protocol

class AdapterQueueConsumerProtocol(Protocol):
    async def consume(self, queue_name: str) -> None:
        ...