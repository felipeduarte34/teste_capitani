from fastapi import FastAPI
from src.api.controllers.product_controller import router as product_router
from src.core.config import create_database

app = FastAPI()

app.include_router(product_router)

@app.on_event("startup")
async def startup():
    await create_database()