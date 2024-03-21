from pydantic import BaseModel, field_validator


class OrderItemSchema(BaseModel):
    product_id: int
    price: int
    quantity: int

    @field_validator('product_id')
    def min_length_validation(cls, v):
        if v < 1:
            raise ValueError("Giá trị không hợp lệ!")
        return v

    @field_validator('price', 'quantity')
    def ge_validation(cls, v):
        if v < 0:
            raise ValueError("Giá trị phải lớn hơn hoặc bằng 0!")
        return v
