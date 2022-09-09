import db
import json
from fastapi import FastAPI

app = FastAPI()

conn = db.get_connection()


@app.get("/api/{entity}")
async def list_entities(entity: str):
    return db.find_all_by_name(conn, entity, timestamp_asc=False)


@app.post("/api/{entity}")
async def post_entity(entity: str, payload: dict):
    _id = db.save_payload(conn, entity, json.dumps(payload))
    return db.find_by_id(conn, _id)
