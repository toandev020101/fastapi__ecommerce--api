from typing import List

from pydantic import BaseModel, field_validator

from app.models.Order import OrderStatus
from app.schemas import OrderItemSchema


class OrderSchema(BaseModel):
    address: str
    phone_number: str
    order_items: List[OrderItemSchema]

    @field_validator('address', 'phone_number')
    def min_length_validation(cls, v):
        if len(v) < 1:
            raise ValueError("Giá trị không được để trống!")
        return v


class ChangeOrderStatusSchema(BaseModel):
    status: OrderStatus

