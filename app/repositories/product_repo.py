from sqlalchemy import select, and_, update as sql_update

from app.core import db, commit_rollback
from app.models import Product
from app.repositories import BaseRepo


class ProductRepository(BaseRepo):
    model = Product

    @staticmethod
    async def find_one_by_name(name: str):
        query = select(Product).where(and_(Product.name == name, Product.is_active == True))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def change_quantity(id: int, new_quantity: int, in_transaction: bool = False):
        query = sql_update(Product).where(and_(Product.id == id, Product.is_active == True)).values(
            quantity=new_quantity).execution_options(synchronize_session="fetch")
        result = await db.execute(query)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()
        return result.rowcount
