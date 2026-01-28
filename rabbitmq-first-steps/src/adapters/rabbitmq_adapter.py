from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Literal
from typing_extensions import Awaitable

from aio_pika.abc import (
    AbstractChannel,
    AbstractRobustConnection, 
    AbstractQueue,
    AbstractExchange,
    AbstractIncomingMessage
)
from aio_pika import connect_robust, Message, ExchangeType
from pydantic import BaseModel


from src.config import settings


class RabbitMQQueueConfig(BaseModel):
    durable: bool = False
    exclusive: bool = False
    passive: bool = False
    auto_delete: bool = False
   


class RabbitMQAdapterInterface(ABC):
    @abstractmethod
    async def connect(self) -> 'RabbitMQAdapterInterface':
        raise NotImplementedError

    @abstractmethod
    async def create_channel(self) -> 'RabbitMQAdapterInterface':
        raise NotImplementedError
    
    @abstractmethod
    async def declare_queue(self, queue_name: str, extra_config: RabbitMQQueueConfig | None = None) -> 'RabbitMQAdapterInterface':
        raise NotImplementedError
    
    @abstractmethod
    async def declare_exchange(self, exchange_name: str,
            *,
            exchange_type: Literal[ExchangeType.DIRECT, ExchangeType.FANOUT, ExchangeType.TOPIC] = ExchangeType.DIRECT) -> 'RabbitMQAdapterInterface':
        raise NotImplementedError
    
    @abstractmethod
    async def bind_queue(self, routing_key: str) -> 'RabbitMQAdapterInterface':
        raise NotImplementedError
    
    @abstractmethod
    async def close_connection(self) -> None:
        raise NotImplementedError
    

class RabbitMQAdapter(RabbitMQAdapterInterface):

    connection: AbstractRobustConnection
    channel: AbstractChannel
    exchange: AbstractExchange | None = None
    queue: AbstractQueue

    async def connect(self) -> 'RabbitMQAdapter':
        self.connection = await connect_robust(settings.RABBITMQ_URL)
        return self
    
    async def create_channel(self) -> 'RabbitMQAdapter':
        self.channel = await self.connection.channel()
        return self
    
    async def declare_exchange(
            self, 
            exchange_name: str, 
            *,
            exchange_type: Literal[ExchangeType.DIRECT, ExchangeType.FANOUT, ExchangeType.TOPIC] = ExchangeType.DIRECT
        ) -> 'RabbitMQAdapter':
        self.exchange = await self.channel.declare_exchange(exchange_name, durable=True, type=exchange_type)
        return self
    
    async def declare_queue(self, queue_name: str, extra_config: RabbitMQQueueConfig | None = None) -> 'RabbitMQAdapter':
        self.queue = await self.channel.declare_queue(queue_name, 
                                         durable=extra_config.durable if extra_config is not None else True,
                                         exclusive=extra_config.exclusive if extra_config is not None else False,
                                         passive=extra_config.passive if extra_config is not None else False,
                                         auto_delete=extra_config.auto_delete if extra_config is not None else False)
        return self
    
    async def bind_queue(self, routing_key: str, *, timeout: float | None = None) -> 'RabbitMQAdapter':
        """Bind the declared queue to the declared exchange with the given routing key."""
        if self.exchange is None:
            raise ValueError("Exchange must be declared before binding queue")
        if getattr(self, 'queue', None) is None:
            raise ValueError("Queue must be declared before binding")
        await self.queue.bind(self.exchange, routing_key=routing_key, timeout=timeout)
        return self

    async def close_connection(self) -> None:
        await self.connection.close()

    
class RabbitMQPublisher:

    def __init__(self, adapter: RabbitMQAdapter):
        self.adapter = adapter

    async def publish(self, routing_key: str, message_body: bytes) -> None:
        exchange = self.adapter.exchange if self.adapter.exchange else self.adapter.channel.default_exchange
        published_status = await exchange.publish(
            Message(body=message_body),
            routing_key=routing_key,
        )
        print(f"Published status: {published_status}")

class RabbitMQConsumer:
    
    def __init__(self, adapter: RabbitMQAdapter):
        self.adapter = adapter

    async def start_consuming(self, on_message_callback: Callable[[AbstractIncomingMessage], Awaitable[None]]) -> None:
        if getattr(self.adapter, 'queue', None) is None:
            raise ValueError("Queue must be declared before starting consumption")
        await self.adapter.queue.consume(on_message_callback)