from typing import Protocol

class AdapterQueueProducerProtocol(Protocol):
    async def publish(self, message: str, queue_name: str) -> None:
        ...