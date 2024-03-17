from sqlalchemy import select, update as sql_update

from app.core import db, commit_rollback
from app.models import User
from app.repositories import BaseRepo


class UserRepository(BaseRepo):
    model = User

    @staticmethod
    async def find_one_by_username(username: str) -> User:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_token_version(id: int, token_version: int):
        query = sql_update(User).where(User.id == id).values(token_version=token_version).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
