from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router as item_router
from app.db import create_collection_if_not_exists, client
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_collection_if_not_exists()
    yield

    client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(item_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=MONGO_HOST, port=8000)
