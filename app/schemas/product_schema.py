from pydantic import BaseModel, field_validator


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity: int

    @field_validator('name', 'description')
    def min_length_validation(cls, v):
        if len(v) < 1:
            raise ValueError("Giá trị không được để trống!")
        return v

    @field_validator('price', 'quantity')
    def ge_validation(cls, v):
        if v < 0:
            raise ValueError("Giá trị phải lớn hơn hoặc bằng 0!")
        return v
