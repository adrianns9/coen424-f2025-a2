import os
import random
import httpx

from fastapi import FastAPI, Request
from dotenv import load_dotenv

USER_V1 = os.getenv("USER_V1")
USER_V2 = os.getenv("USER_V2")
P = float(os.getenv("P", 0.5))


def pick_user_service():
    """Return URL of v1 or v2 based on probability P."""
    return USER_V1 if random.random() < P else USER_V2


load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {'hello': True}


# User Microservices
@app.post("/users")
async def create_user(request: Request):
    service = pick_user_service()

    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.post(
            f"{service}/users",
            json=forward_body
        )
        return resp.json()


@app.put("/users/{user_id}")
async def update_user(user_id: str, request: Request):
    service = pick_user_service()

    async with httpx.AsyncClient() as client:
        forward_body = await request.json()
        resp = await client.put(
            f"{service}/users/{user_id}",
            json=forward_body
        )
        return resp.json()

# Order Microservices
# @app.get("/orders")
# async def get_order():
#     pass
#
#
# @app.post("/orders")
# async def create_order():
#     pass
#
#
# @app.put("/orders/{order_id}")
# async def get_order(order_id):
#     pass
