from pydantic import BaseModel, constr, field_validator


class LoginSchema(BaseModel):
    username: constr(strip_whitespace=True, min_length=4)
    password: constr(strip_whitespace=True, min_length=6)

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
