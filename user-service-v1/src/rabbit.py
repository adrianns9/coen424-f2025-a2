import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")


async def get_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)


async def publish_message(queue_name: str, message: dict, headers: dict = None):
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=str(message).encode(),
                headers=headers or {},
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue_name
        )
