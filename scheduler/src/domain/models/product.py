from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: str
    name: str
    description: str
    pricing: dict
    availability: dict
    category: str