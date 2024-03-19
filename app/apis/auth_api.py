from fastapi import APIRouter, Request, Response, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core import get_settings
from app.repositories import JWTBearer
from app.schemas import ResponseSchema, RegisterSchema, LoginSchema
from app.services import AuthService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/auth", tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema)
async def register(request_body: RegisterSchema, response: Response):
    result = await AuthService.register(schema=request_body, response=response)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Đăng ký thành công", result=result)


@router.post("/login", response_model=ResponseSchema)
async def login(request_body: LoginSchema, response: Response):
    result = await AuthService.login(schema=request_body, response=response)
    return ResponseSchema(status_code=status.HTTP_200_OK,
                          detail="Đăng nhập thành công",
                          result=result
                          )


@router.get("/refresh-token", response_model=ResponseSchema)
async def refresh_token(request: Request, response: Response):
    result = await AuthService.refresh_token(request=request, response=response)
    return ResponseSchema(status_code=status.HTTP_200_OK,
                          detail="Lấy refresh token thành công",
                          result=result
                          )


@router.get("/logout", response_model=ResponseSchema)
async def logout(response: Response, user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    await AuthService.logout(response=response, user_decode=user_decode)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Đăng xuất thành công")
