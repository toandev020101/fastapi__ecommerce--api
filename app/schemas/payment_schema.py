from pydantic import BaseModel, field_validator


class ProcessPaymentSchema(BaseModel):
    amount_money: int

    @field_validator('amount_money')
    def ge_validation(cls, v):
        if v < 0:
            raise ValueError("Giá trị phải lớn hơn hoặc bằng 0!")
        return v
