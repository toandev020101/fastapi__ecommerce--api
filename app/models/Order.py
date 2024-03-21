from enum import Enum as PythonEnum

from sqlalchemy import Column, Integer, Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models import BaseModel


class OrderStatus(PythonEnum):
    PENDING = "Chờ lấy hàng"
    SHIPPING = "Đang vận chuyển"
    COMPLETED = "Đã hoàn thành"
    CANCELLED = "Đã hủy"


status_values = [member.value for member in OrderStatus.__members__.values()]


class Order(BaseModel):
    __tablename__ = "orders"

    address = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=False)

    total_price = Column(Integer, default=0, server_default="0", nullable=False)
    total_quantity = Column(Integer, default=0, server_default="0", nullable=False)

    status = Column(Enum(*status_values, name='order_status'), default=OrderStatus.PENDING.value,
                    server_default=OrderStatus.PENDING.value, nullable=False)
    is_paid = Column(Boolean, default=False, server_default="false", nullable=False)
    is_active = Column(Boolean, default=True, server_default="true", nullable=False)

    order_items = relationship("OrderItem", back_populates="order", lazy="selectin")

    buyer_id = Column(Integer, ForeignKey('users.id'))
    buyer = relationship("User", back_populates="orders", lazy="selectin")
