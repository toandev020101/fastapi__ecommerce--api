from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(150), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, default=0, server_default="0", nullable=False)
    quantity = Column(Integer, default=0, server_default="0", nullable=False)
    is_active = Column(Boolean, default=True, server_default="true", nullable=False)

    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="products", lazy="selectin")

    order_items = relationship("OrderItem", back_populates="product", lazy="selectin")
