from src.adapters.rabbitmq_adapter import RabbitMQAdapter, RabbitMQPublisher
import asyncio
import aio_pika

from src.config import settings


rabbitmq_adapter = RabbitMQAdapter()
publisher = RabbitMQPublisher(rabbitmq_adapter)

async def main():
    await rabbitmq_adapter.connect()
    await rabbitmq_adapter.create_channel()
    await rabbitmq_adapter.declare_exchange(settings.RABBITMQ_EXCHANGE_NAME, exchange_type=aio_pika.ExchangeType.TOPIC)
    await rabbitmq_adapter.declare_queue(settings.RABBITMQ_QUEUE_NAME)
    await rabbitmq_adapter.bind_queue(routing_key="my_routing_key")  # Bind queue to exchange
    print(f"Queue '{settings.RABBITMQ_QUEUE_NAME}' bound to exchange '{settings.RABBITMQ_EXCHANGE_NAME}' with routing key 'my_routing_key'")

    while True:
        message = input("Enter a message to publish (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        await publisher.publish(
            routing_key="my_routing_key",
            message_body=message.encode()
        )
        print(f" [x] Sent '{message}'")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        asyncio.run(rabbitmq_adapter.close_connection())    