from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
from pymongo import MongoClient

app = FastAPI()

# Redis setup
redis_client = Redis(host='localhost', port=6379, db=0)

# MongoDB setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['mydatabase']
collection = db['mycollection']

class Item(BaseModel):
    id: int
    name: str
    description: str

@app.post("/items/")
async def create_item(item: Item):
    # Insert into MongoDB
    collection.insert_one(item.dict())
    # Cache in Redis
    redis_client.set(item.id, item.json())
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Try to get from Redis
    item = redis_client.get(item_id)
    if item:
        return Item.parse_raw(item)
    # Fallback to MongoDB
    item = collection.find_one({"id": item_id})
    if item:
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # Update in MongoDB
    result = collection.update_one({"id": item_id}, {"$set": item.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    # Update in Redis
    redis_client.set(item_id, item.json())
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # Delete from MongoDB
    result = collection.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    # Delete from Redis
    redis_client.delete(item_id)
    return {"detail": "Item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)