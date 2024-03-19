from sqlalchemy import select

from app.core import db
from app.models import Product
from app.repositories import BaseRepo


class ProductRepository(BaseRepo):
    model = Product

    @staticmethod
    async def find_one_by_name(name: str):
        query = select(Product).where(Product.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
