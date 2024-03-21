from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    price = Column(Integer, default=0, server_default="0", nullable=False)
    quantity = Column(Integer, default=0, server_default="0", nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="order_items", lazy="selectin")

    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="order_items", lazy="selectin")
