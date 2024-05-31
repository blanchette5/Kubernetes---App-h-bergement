from fastapi import FastAPI
import redis
import os
app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

@app.get("/")
def status():
    return {"status": "OK"}

@app.get("/get_data_from_redis/{key}")
def read_item(key: str):
    value = redis_client.get(key)
    if value:
        return {"key": key, "value": value.decode('utf-8')}
    else:
        return {"key": key, "value": "Key not found"}

@app.post("/set_item/{key}/{value}")
def set_item(key: str, value: str):
    redis_client.set(key, value)
    return {"message": "Item set successfully", "key": key, "value": value}