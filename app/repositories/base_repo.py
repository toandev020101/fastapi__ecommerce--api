from typing import Generic, TypeVar, List

from pydantic import BaseModel
from sqlalchemy import update as sql_update, delete as sql_delete, select

from app.core import db, commit_rollback

T = TypeVar('T')


class BaseRepo:
    model = Generic[T]

    @classmethod
    async def find_all(cls):
        query = select(cls.model)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_by_id(cls, id: int):
        query = select(cls.model).where(cls.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create_one(cls, new_model: BaseModel):
        obj = cls.model(**new_model.to_dict())
        db.add(obj)
        await commit_rollback()
        await db.refresh(obj)
        return obj

    @classmethod
    async def update_one(cls, id: int, new_model: BaseModel):
        query = sql_update(cls.model).where(cls.model.id == id).values(
            **new_model.to_dict()).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

        updated_obj = await cls.find_one_by_id(id)
        return updated_obj

    @classmethod
    async def delete_one(cls, id: int):
        query = sql_delete(cls.model).where(cls.model.id == id)
        result = await db.execute(query)
        await commit_rollback()
        return result.rowcount

    @classmethod
    async def delete_list(cls, ids: List[int]):
        query = sql_delete(cls.model).where(cls.model.id.in_(ids))
        result = await db.execute(query)
        await commit_rollback()
        return result.rowcount
