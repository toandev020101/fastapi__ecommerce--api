import re
from typing import TypeVar

from pydantic import BaseModel, EmailStr, constr, field_validator

T = TypeVar('T')


class RegisterSchema(BaseModel):
    full_name: constr(strip_whitespace=True, min_length=4)
    username: constr(strip_whitespace=True, min_length=4)
    password: constr(strip_whitespace=True, min_length=6)
    email: str

    @field_validator('email')
    def email_validation(cls, v):
        regex = r'^\S+@\S+\.\S+$'
        if not re.match(regex, v):
            raise ValueError("Email không hợp lệ!")
        return v

    @field_validator('full_name', 'username', 'password')
    def min_length_validation(cls, v):
        if len(v) < 1:
            raise ValueError("Giá trị không được để trống!")
        return v

    @field_validator('password')
    def password_length_validation(cls, v):
        if len(v) < 6:
            raise ValueError("Mật khẩu phải chứa ít nhất 6 ký tự!")
        return v
