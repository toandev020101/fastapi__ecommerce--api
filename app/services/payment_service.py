from fastapi import HTTPException, status

from app.core import db
from app.models.Order import OrderStatus
from app.models.Payment import PaymentMethod, PaymentStatus
from app.repositories import PaymentRepository, OrderRepository
from app.schemas import ProcessPaymentSchema


class PaymentService:

    @staticmethod
    async def get_all():
        objects = await PaymentRepository.find_all()
        new_objects = []
        for obj in objects:
            new_objects.append(obj.to_dict(relationships=["order"]))
        return new_objects

    @staticmethod
    async def get_one_by_id(id: int):
        # check payment
        payment = await PaymentRepository.find_one_by_id(id=id)

        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy thanh toán!")

        return payment.to_dict(relationships=["order"])

    @staticmethod
    async def process_payment(id: int, schema: ProcessPaymentSchema):
        # check payment
        payment = await PaymentRepository.find_one_by_id(id=id)

        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy thanh toán!")

        if payment.payment_method == PaymentMethod.PAYMENT_ON_DELIVERY.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Thanh toán không hợp lệ!")

        if schema.amount_money < payment.amount_money or schema.amount_money > payment.amount_money:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Số tiền thanh toán không hợp lệ!")

        try:
            await OrderRepository.change_status(id=payment.order.id, status=OrderStatus.PENDING.value,
                                                in_transaction=True)
            await PaymentRepository.change_status(id=payment.id, status=PaymentStatus.SUCCESS.value)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Lỗi máy chủ: {e}")
