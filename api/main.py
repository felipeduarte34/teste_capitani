from fastapi import FastAPI
from src.api.controllers.product_controller import router
from src.core.config import create_database

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    await create_database()