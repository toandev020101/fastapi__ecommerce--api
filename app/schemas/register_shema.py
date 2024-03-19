import re
from typing import TypeVar

from pydantic import BaseModel, EmailStr, field_validator

T = TypeVar('T')


class RegisterSchema(BaseModel):
    full_name: str
    username: str
    password: str
    email: EmailStr

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
