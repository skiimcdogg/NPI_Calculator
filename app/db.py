from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

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

calculations_collection = database.get_collection("calculations")
