import os
import random
import httpx
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

# User service URLs
USER_V1 = os.getenv("USER_V1")
USER_V2 = os.getenv("USER_V2")
P = float(os.getenv("P", 0.5))

# Order service URL
ORDER_SERVICE = os.getenv("ORDER_SERVICE")


def pick_user_service():
    """Return URL of v1 or v2 based on probability P."""
    return USER_V1 if random.random() < P else USER_V2


app = FastAPI()


@app.get("/")
async def root():
    return {'hello': True}


# ----------------------
# User Microservices
# ----------------------
@app.post("/users")
async def create_user(request: Request):
    service = pick_user_service()
    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.post(f"{service}/users", json=forward_body)
        return resp.json()


@app.put("/users/{user_id}")
async def update_user(user_id: str, request: Request):
    service = pick_user_service()
    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.put(f"{service}/users/{user_id}", json=forward_body)
        return resp.json()


# ----------------------
# Order Microservices
# ----------------------
@app.post("/orders")
async def create_order(request: Request):
    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.post(f"{ORDER_SERVICE}/orders", json=forward_body)
        return resp.json()


@app.get("/orders")
async def get_orders(status: str = None):
    params = {"status": status} if status else {}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORDER_SERVICE}/orders", params=params)
        return resp.json()


@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.put(f"{ORDER_SERVICE}/orders/{order_id}/status", json=forward_body)
        return resp.json()


@app.put("/orders/{order_id}/contact")
async def update_order_contact(order_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.put(f"{ORDER_SERVICE}/orders/{order_id}/contact", json=forward_body)
        return resp.json()
