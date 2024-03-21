from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
from pydantic import BaseModel as PydanticBaseModel

from app.core import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
                         server_onupdate=func.now(),
                         nullable=False)

    @staticmethod
    def extra_relationships(model):
        result = {}
        for item in model.__table__.columns:
            if item.name != "password":
                result[item.name] = getattr(model, item.name)
        return result

    def to_dict(self, relationships=None):
        columns = self.__mapper__.columns

        result = {}
        # Lấy giá trị của các cột
        for column in columns:
            if column.key != "password":
                result[column.key] = getattr(self, column.key)

        # Lấy giá trị của các relationship nếu được chỉ định
        if relationships:
            for relationship_name in relationships:
                if hasattr(self, relationship_name):
                    value = getattr(self, relationship_name)
                    if value is not None:
                        if isinstance(value, list):
                            result[relationship_name] = [self.extra_relationships(item) for item in value]
                        else:
                            result[relationship_name] = self.extra_relationships(value)

        return result
