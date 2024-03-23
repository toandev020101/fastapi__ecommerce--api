from sqlalchemy import update as sql_update, and_

from app.core import db, commit_rollback
from app.models import Payment
from app.repositories import BaseRepo


class PaymentRepository(BaseRepo):
    model = Payment

    @staticmethod
    async def change_status(id: int, status: str, in_transaction: bool = False):
        query = sql_update(Payment).where(
            and_(Payment.id == id, Payment.is_active == True)).values(status=status).execution_options(
            synchronize_session="fetch")
        result = await db.execute(query)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()
        return result.rowcount
