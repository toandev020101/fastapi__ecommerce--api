from sqlalchemy import select, update as sql_update, and_

from app.core import db
from app.models import User
from app.repositories import BaseRepo


class UserRepository(BaseRepo):
    model = User

    @staticmethod
    async def find_one_by_username(username: str) -> User:
        query = select(User).where(and_(User.username == username, User.is_active == True))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_token_version(id: int, token_version: int):
        query = sql_update(User).where(and_(User.id == id, User.is_active == True)).values(
            token_version=token_version).execution_options(synchronize_session="fetch")
        await db.execute(query)
