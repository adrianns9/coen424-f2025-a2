from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {'hello': True}


@app.put("/users/{user_id}")
async def update_user(user_id):
    return {}


@app.post("/users")
async def create_user():
    return {}
