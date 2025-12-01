import json


async def handle_user_contact_updated(body: bytes):
    """
    body is bytes containing JSON event payload from User Microservice.
    Example event:
    {
       "event_id": "...",
       "type": "user.contact.updated",
       "user_id": "...",
       "email": "...",
       "delivery_address": "...",
       "version": "v1"
    }
    """
    event = json.loads(body.decode())
    print("\n--- Received Event ---")
    print(event)
    print("----------------------\n")

    # TODO (next step):
    # update all orders belonging to user_id in Order Microservice DB
    # Example:
    # await orders_collection.update_many(
    #     {"user_id": event["user_id"]},
    #     {"$set": {
    #         "email": event["email"],
    #         "delivery_address": event["delivery_address"]
    #     }}
    # )
