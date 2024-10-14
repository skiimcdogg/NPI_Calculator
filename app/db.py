from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "rootpassword")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_INITDB_DATABASE", "mydatabase")

MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"

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
