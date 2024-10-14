from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router as item_router
from app.db import create_collection_if_not_exists, client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_collection_if_not_exists()
    yield

    client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(item_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
