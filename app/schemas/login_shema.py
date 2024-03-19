from pydantic import BaseModel, constr, field_validator


class LoginSchema(BaseModel):
    username: str
    password: str

    @field_validator('username', 'password')
    def min_length_validation(cls, v):
        if len(v) < 1:
            raise ValueError("Giá trị không được để trống!")
        return v

    @field_validator('password')
    def password_length_validation(cls, v):
        if len(v) < 6:
            raise ValueError("Mật khẩu phải chứa ít nhất 6 ký tự!")
        return v
