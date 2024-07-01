from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.models.product import Product, ProductSchema

async def create_product(db: AsyncSession, product: ProductSchema):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()