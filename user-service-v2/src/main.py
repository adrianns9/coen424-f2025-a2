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
        "service_version": "v2",
    }

    await users_collection.insert_one(user_doc)
    return user_doc


@app.put("/users/{user_id}")
async def update_user(user_id: str, payload: UserUpdate):
    """
    Update User Information.
    Args:
        user_id: User ID
        payload: User Update
    """
    existing = await users_collection.find_one({"_id": user_id})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {}
    info_changed = False

    # Detect actual changes
    if payload.email is not None and payload.email != existing["email"]:
        update_data["email"] = payload.email
        info_changed = True

    if payload.delivery_address is not None and payload.delivery_address != existing["delivery_address"]:
        update_data["delivery_address"] = payload.delivery_address
        info_changed = True

    # Always keep version tag up to date
    update_data["service_version"] = "v2"

    # Perform update only if something changed
    if update_data:
        await users_collection.update_one({"_id": user_id}, {"$set": update_data})

    # Publish event ONLY if contact info changed
    if info_changed:
        event_message = {
            "user_id": user_id,
            "email": update_data.get("email", existing["email"]),
            "delivery_address": update_data.get("delivery_address", existing["delivery_address"]),
        }
        await publish_message(
            message=event_message,
            headers={"type": "user.contact.updated"}
        )

    updated = await users_collection.find_one({"_id": user_id})
    return {
        "id": updated["_id"],
        "email": updated["email"],
        "delivery_address": updated["delivery_address"],
        "service_version": updated["service_version"],
    }
