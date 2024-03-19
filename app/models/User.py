from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from app.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name = Column(String(100), nullable=False)
    username = Column(String(65), unique=True, nullable=False)
    password = Column(String(65), nullable=False)
    email = Column(String(150), nullable=True)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    token_version = Column(Integer, default=0, server_default="0", nullable=False)

    products = relationship("Product", back_populates="creator")