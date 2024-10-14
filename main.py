# main.py
from fastapi import FastAPI
from app.routes import router as item_router
from app.db import create_collection_if_not_exists

app = FastAPI()

@app.lifespan("startup")
async def startup_db_client():
    await create_collection_if_not_exists()

# Inclure les routes
app.include_router(item_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
