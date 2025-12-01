import asyncio
from rabbit import setup_channel
from handlers import handle_user_contact_updated


async def consume_events():
    connection, channel, queue = await setup_channel()

    print("📡 Event System is listening for events...")

    async with connection:
        async with channel:
            async for message in queue:
                async with message.process():
                    event_type = None

                    try:
                        event_type = message.headers.get("type", None)
                    except:
                        pass

                    # For now, treat all messages as "user.contact.updated"
                    await handle_user_contact_updated(message.body)


if __name__ == "__main__":
    try:
        asyncio.run(consume_events())
    except KeyboardInterrupt:
        print("Event system shutting down.")
