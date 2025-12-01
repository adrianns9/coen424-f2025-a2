from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schemas import UserCreate, UserUpdate
from user_db import users_collection
from rabbit import publish_message
import uuid

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": True}


@app.post("/users")
async def create_user(payload: UserCreate):
    user_id = str(uuid.uuid4())

    user_doc = {
        "_id": user_id,
        "email": payload.email,
        "delivery_address": payload.delivery_address,
    }

    await users_collection.insert_one(user_doc)
    return user_doc


@app.put("/users/{user_id}")
async def update_user(user_id: str, payload: UserUpdate):
    existing = await users_collection.find_one({"_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {}
    if payload.email is not None:
        update_data["email"] = payload.email
    if payload.delivery_address is not None:
        update_data["delivery_address"] = payload.delivery_address

    if update_data:
        await users_collection.update_one({"_id": user_id}, {"$set": update_data})

        # Publish event to RabbitMQ
        event_message = {
            "user_id": user_id,
            "email": update_data.get("email", existing["email"]),
            "delivery_address": update_data.get("delivery_address", existing["delivery_address"]),
        }
        await publish_message(
            queue_name="user_events",
            message=event_message,
            headers={"type": "user.contact.updated"}
        )

    updated = await users_collection.find_one({"_id": user_id})
    return {
        "id": updated["_id"],
        "email": updated["email"],
        "delivery_address": updated["delivery_address"],
    }
