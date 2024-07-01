from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.domain.models.product import Product, ProductSchema
from src.services.product_service import create_product, get_products
from src.services.kafka_producer_service import produce_message

router = APIRouter()

@router.post("/products/", response_model=ProductSchema)
async def add_product(product: ProductSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    try:
        new_product = await create_product(db, product)

        #utilizando background tasks para enviar a mensagem para o kafka
        background_tasks.add_task(produce_message, product.dict())

        return new_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/", response_model=list[ProductSchema])
async def read_products(db: AsyncSession = Depends(get_db)):
    try:
        products = await get_products(db)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))