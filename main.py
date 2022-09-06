from fastapi import FastAPI
from collections import defaultdict

app = FastAPI()

storage = defaultdict(list)

@app.get("/api/{entity}")
async def list_entities(entity: str):
    return storage[entity]

@app.post("/api/{entity}")
async def post_entitity(entity: str, payload: dict):
    storage[entity].append(payload)
    return payload