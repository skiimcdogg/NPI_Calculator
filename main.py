# main.py
from fastapi import FastAPI
from app.routes import router as item_router

app = FastAPI()

# Inclure les routes
app.include_router(item_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
