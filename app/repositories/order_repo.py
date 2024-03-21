from sqlalchemy import select, and_, update as sql_update

from app.core import db, commit_rollback
from app.models import Order
from app.repositories import BaseRepo


class OrderRepository(BaseRepo):
    model = Order

    @staticmethod
    async def find_list_by_buyer_id(buyer_id: int):
        query = select(Order).where(and_(Order.buyer_id == buyer_id, Order.is_active == True))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def change_status(id: int, status: str, in_transaction: bool = False):
        query = sql_update(Order).where(
            and_(Order.id == id, Order.is_active == True)).values(status=status).execution_options(
            synchronize_session="fetch")
        result = await db.execute(query)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()
        return result.rowcount
