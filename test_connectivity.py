from redis import Redis
from pymongo import MongoClient

def test_redis_connection():
    try:
        redis_client = Redis(host='localhost', port=6379, db=0)
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")
        if value == b"test_value":
            print("Redis connection successful.")
        else:
            print("Redis connection failed.")
    except Exception as e:
        print(f"Redis connection error: {e}")

def test_mongo_connection():
    try:
        mongo_client = MongoClient('mongodb://localhost:27017/')
        db = mongo_client['mydatabase']
        collection = db['mycollection']
        collection.insert_one({"test_key": "test_value"})
        document = collection.find_one({"test_key": "test_value"})
        if document and document["test_key"] == "test_value":
            print("MongoDB connection successful.")
        else:
            print("MongoDB connection failed.")
    except Exception as e:
        print(f"MongoDB connection error: {e}")

if __name__ == "__main__":
    print("Testing Redis connection...")
    test_redis_connection()
    print("Testing MongoDB connection...")
    test_mongo_connection()