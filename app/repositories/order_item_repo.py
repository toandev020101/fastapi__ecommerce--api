from sqlalchemy import select

from app.core import db
from app.models import OrderItem
from app.repositories import BaseRepo


class OrderItemRepository(BaseRepo):
    model = OrderItem

    @staticmethod
    async def find_list_by_order_id(order_id: int):
        query = select(OrderItem).where(OrderItem.order_id == order_id)
        result = await db.execute(query)
        return result.scalars().all()
