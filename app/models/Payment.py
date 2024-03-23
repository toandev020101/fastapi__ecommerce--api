from enum import Enum as PythonEnum

from sqlalchemy import Column, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from app.models import BaseModel


class PaymentStatus(PythonEnum):
    PENDING = "Đang chờ xử lý"
    SUCCESS = "Thành công"
    FAILURE = "Thất bại"
    REFUND = "Hoàn tiền"


status_values = [member.value for member in PaymentStatus.__members__.values()]


class PaymentMethod(PythonEnum):
    PAYMENT_ON_DELIVERY = "Thanh toán khi nhận hàng"
    PAYMENT_BY_BANK = "Thanh toán bằng ngân hàng"
    PAYMENT_BY_MOMO = "Thanh toán bằng ví momo"


payment_method_values = [member.value for member in PaymentMethod.__members__.values()]


class Payment(BaseModel):
    __tablename__ = "payments"

    amount_money = Column(Integer, default=0, server_default="0", nullable=False)
    status = Column(Enum(*status_values, name='payment_status'), default=PaymentStatus.PENDING.value,
                    server_default=PaymentStatus.PENDING.value, nullable=False)
    payment_method = Column(Enum(*payment_method_values, name='payment_method'),
                            default=PaymentMethod.PAYMENT_ON_DELIVERY.value,
                            server_default=PaymentMethod.PAYMENT_ON_DELIVERY.value, nullable=False)
    is_active = Column(Boolean, default=True, server_default="true", nullable=False)

    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="payment", lazy="selectin")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="payments", lazy="selectin")
