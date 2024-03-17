from typing import Optional
from datetime import timedelta, datetime

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from fastapi import Request, Response, status, HTTPException
from passlib.context import CryptContext

from app.core import get_settings
from app.models import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hashing:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)


class JWTRepo:
    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        # Prepare the data to be encoded in the JWT
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"iat": datetime.utcnow()})
        to_encode.update({"exp": expire})

        # Generate and return the JWT token
        encode_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        return encode_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            # Attempt to decode the token, and check for expiration
            decode_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
            return decode_token if datetime.utcfromtimestamp(decode_token["exp"]) >= datetime.utcnow() else None
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.JWTError:
            # Handle other JWT errors
            return {}

    @staticmethod
    def create_access_token(user: User):
        return (JWTRepo.generate_token(data={"user_id": user.id, "username": user.username},
                                       expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)))

    @staticmethod
    def send_refresh_token(response: Response, user: User):
        refresh_token = (
            JWTRepo.generate_token(
                data={"user_id": user.id, "username": user.username, "token_version": user.token_version},
                expires_delta=timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)))

        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path=f"{settings.BASE_API_SLUG}/auth/refresh-token"
        )

    @staticmethod
    def clear_refresh_token(response: Response):
        response.delete_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            httponly=True,
            secure=True,
            samesite="lax",
            path=f"{settings.BASE_API_SLUG}/auth/refresh-token"
        )


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # Validate and extract JWT token from the request
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                # Return Forbidden if the authentication scheme is not Bearer
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"status": "Forbidden", "message": "Token không hợp lệ!"}
                )
            if not self.verify_jwt(token=credentials.credentials):
                # Return Forbidden if the token is invalid or expired
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"status": "Forbidden", "message": "Token không hợp lệ hoặc đã hết hạn!"}
                )
            return JWTRepo.decode_token(token=credentials.credentials)
        else:
            # Return Forbidden if there are no valid credentials
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "Forbidden", "message": "Lỗi hệ thống!"}
            )

    @staticmethod
    def verify_jwt(token: str):
        # Verify the JWT token
        try:
            JWTRepo.decode_token(token=token)
            return True
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return False
        except jwt.JWTError:
            # Handle other JWT errors
            return False
