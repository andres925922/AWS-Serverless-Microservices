from src.adapters.rabbitmq_adapter import RabbitMQAdapter, RabbitMQConsumer
import asyncio
from aio_pika.abc import AbstractIncomingMessage
import aio_pika
from typing_extensions import Awaitable

from src.config import settings


rabbitmq_adapter = RabbitMQAdapter()
consumer = RabbitMQConsumer(rabbitmq_adapter)

async def on_message(message: AbstractIncomingMessage):
    print(message.body_size)
    async with message.process():
        print(f" [x] Received: {message.body.decode()}")

async def main():
    await rabbitmq_adapter.connect()
    await rabbitmq_adapter.create_channel()
    await rabbitmq_adapter.declare_exchange(settings.RABBITMQ_EXCHANGE_NAME, exchange_type=aio_pika.ExchangeType.TOPIC)
    await rabbitmq_adapter.declare_queue(settings.RABBITMQ_QUEUE_NAME)
    await rabbitmq_adapter.bind_queue(routing_key="my_routing_key")
    
    print(f"Waiting for messages on queue '{settings.RABBITMQ_QUEUE_NAME}'...")
    print("Press CTRL+C to exit")
    
    # Start consuming messages
    await consumer.start_consuming(on_message) 
    
    # Keep the consumer running
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        asyncio.run(rabbitmq_adapter.close_connection())
