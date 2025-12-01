from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from schemas import OrderCreate, OrderUpdateStatus, OrderUpdateContact
from order_db import orders_collection
import uuid

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": True}


@app.post("/orders")
async def create_order(payload: OrderCreate):
    order_id = str(uuid.uuid4())
    order_doc = {
        "_id": order_id,
        "email": payload.email,
        "delivery_address": payload.delivery_address,
        "items": [item.dict() for item in payload.items],
        "status": "under process"
    }

    await orders_collection.insert_one(order_doc)
    return order_doc


@app.get("/orders")
async def get_orders(status: str = Query(None, description="Filter orders by status")):
    query = {"status": status} if status else {}
    orders = await orders_collection.find(query).to_list(100)
    return orders


@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, payload: OrderUpdateStatus):
    existing = await orders_collection.find_one({"_id": order_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")

    await orders_collection.update_one({"_id": order_id}, {"$set": {"status": payload.status}})
    updated = await orders_collection.find_one({"_id": order_id})
    return updated


@app.put("/orders/{order_id}/contact")
async def update_order_contact(order_id: str, payload: OrderUpdateContact):
    existing = await orders_collection.find_one({"_id": order_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = {}
    if payload.email:
        update_data["email"] = payload.email
    if payload.delivery_address:
        update_data["delivery_address"] = payload.delivery_address

    if update_data:
        await orders_collection.update_one({"_id": order_id}, {"$set": update_data})

    updated = await orders_collection.find_one({"_id": order_id})
    return updated
