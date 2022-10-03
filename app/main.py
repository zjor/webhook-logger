from app import db
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

conn = db.get_connection()


@app.on_event("startup")
async def startup_event():
    db.update_schema()


@app.get('/')
async def index():
    return {
        'title': 'Webhook Logger',
        'swagger-ui': '/docs',
        'redoc': '/redoc',
        'example': '/api/example',
        'schemaVersion': db.get_schema_version(conn),
        'stats': {
            'namesCount': db.get_names_count(conn),
            'total': db.get_total_count(conn)
        }
    }


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')


@app.get("/api/{entity}")
async def list_entities(entity: str, limit: int = None):
    return db.find_all_by_name(conn, entity, limit, timestamp_asc=False)


@app.get("/api/{entity}/{_id}")
async def list_entities(entity: str, _id: str):
    obj = db.find_by_id(conn, _id)
    if obj and obj['name'] == entity:
        return obj
    else:
        raise HTTPException(status_code=404, detail=f"{entity} with {_id} was not found")


@app.post("/api/{entity}")
async def post_entity(entity: str, payload: dict, req: Request):
    headers = {}
    for k in req.headers.keys():
        headers[k] = req.headers.get(k)

    _id = db.save_payload(conn, entity, json.dumps(payload), json.dumps(headers))
    return db.find_by_id(conn, _id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
