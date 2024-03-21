from typing import Generic, TypeVar, List

from pydantic import BaseModel
from sqlalchemy import update as sql_update, select, and_

from app.core import db, commit_rollback

T = TypeVar('T')


class BaseRepo:
    model = Generic[T]

    @classmethod
    async def find_all(cls):
        query = select(cls.model).where(cls.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_by_id(cls, id: int):
        query = select(cls.model).where(and_(cls.model.id == id, cls.model.is_active == True))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def create_list(cls, new_models: List[BaseModel], in_transaction: bool = False):
        objs = []
        for new_model in new_models:
            obj = cls.model(**new_model.to_dict())
            objs.append(obj)

        db.add_all(objs)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()

        for obj in objs:
            await db.refresh(obj)

        return objs

    @classmethod
    async def create_one(cls, new_model: BaseModel, in_transaction: bool = False):
        obj = cls.model(**new_model.to_dict())
        db.add(obj)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()

        await db.refresh(obj)
        return obj

    @classmethod
    async def update_one(cls, id: int, new_model: BaseModel, in_transaction: bool = False):
        query = sql_update(cls.model).where(cls.model.id == id).values(
            **new_model.to_dict()).execution_options(synchronize_session="fetch")
        await db.execute(query)

        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()

        updated_obj = await cls.find_one_by_id(id)
        return updated_obj

    @classmethod
    async def delete_one(cls, id: int, in_transaction: bool = False):
        query = sql_update(cls.model).where(and_(cls.model.id == id, cls.model.is_active == True)).values(
            is_active=False).execution_options(synchronize_session="fetch")
        result = await db.execute(query)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()
        return result.rowcount

    @classmethod
    async def delete_list(cls, ids: List[int], in_transaction: bool = False):
        query = sql_update(cls.model).where(and_(cls.model.id.in_(ids), cls.model.is_active == True)).values(
            is_active=False).execution_options(synchronize_session="fetch")
        result = await db.execute(query)
        if in_transaction:
            await db.flush()
        else:
            await commit_rollback()
        return result.rowcount
