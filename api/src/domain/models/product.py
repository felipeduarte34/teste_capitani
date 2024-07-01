from sqlalchemy import Column, String, JSON
from src.core.config import Base
from pydantic import BaseModel

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    pricing = Column(JSON)
    availability = Column(JSON)
    category = Column(String)

class ProductSchema(BaseModel):
    id: str
    name: str
    description: str
    pricing: dict
    availability: dict
    category: str

    class Config:
        from_attributes = True