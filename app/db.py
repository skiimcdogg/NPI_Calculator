from motor.motor_asyncio import AsyncIOMotorClient
import os

# MONGO_USER = os.getenv("MONGO_I
MONGO_INITDB_ROOT_USERNAME = "root"
MONGO_INITDB_ROOT_PASSWORD = "root" # [ ] envs
MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_DB_NAME = "calculations"

MONGO_DETAILS = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin"
print(MONGO_DETAILS)

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[MONGO_DB_NAME]

async def create_collection_if_not_exists():
    collection_name = "calculations"
    collections = await database.list_collection_names()
    if collection_name not in collections:
        await database.create_collection(collection_name)
        print(f"Collection '{collection_name}' created in DB '{MONGO_DB_NAME}'.")

# Collection des calculs
calculations_collection = database.get_collection("calculations")
