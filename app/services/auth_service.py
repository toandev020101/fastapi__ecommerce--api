from fastapi import Request, Response, HTTPException, status

from app.core import get_settings
from app.models import User
from app.repositories import UserRepository, Hashing, JWTRepo
from app.schemas import RegisterSchema, LoginSchema

settings = get_settings()


class AuthService:
    @staticmethod
    async def register(schema: RegisterSchema, response: Response):
        # check username
        user = await UserRepository.find_one_by_username(username=schema.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"username": "Tên người dùng đã tồn tại!"})

        # create user object
        new_user = User(
            full_name=schema.full_name,
            username=schema.username,
            password=Hashing.hash_password(password=schema.password),
            email=schema.email,
        )

        # insert to table
        created_user = await UserRepository.create_one(new_model=new_user)
        # generate token
        access_token = JWTRepo.create_access_token(user=created_user)

        # send refresh token
        JWTRepo.send_refresh_token(response=response, user=created_user)
        return {"data": created_user.to_dict(), "access_token": access_token}

    @staticmethod
    async def login(schema: LoginSchema, response: Response):
        # check user
        user = await UserRepository.find_one_by_username(schema.username)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tên người dùng hoặc mật khẩu không chính xác!")

        if not Hashing.verify_password(schema.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Tên người dùng hoặc mật khẩu không chính xác!")

        # generate token
        access_token = JWTRepo.create_access_token(user)

        # send refresh token
        JWTRepo.send_refresh_token(response=response, user=user)

        return {"data": user.to_dict(), "access_token": access_token}

    @staticmethod
    async def refresh_token(request: Request, response: Response):
        token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

        try:
            user_decode = JWTRepo.decode_token(token=token)
            user = await UserRepository.find_one_by_id(id=int(user_decode['user_id']))
            if not user or user.token_version != user_decode['token_version']:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

            access_token = JWTRepo.create_access_token(user=user)

            # send refresh token
            JWTRepo.send_refresh_token(response=response, user=user)
            return {"access_token": access_token}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ!")

    @staticmethod
    async def logout(response: Response, user_decode: dict):
        # check username
        user = await UserRepository.find_one_by_id(id=user_decode.get('user_id'))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng không tồn tại!")

        await UserRepository.update_token_version(id=user.id, token_version=user.token_version + 1)
        JWTRepo.clear_refresh_token(response=response)

    @staticmethod
    async def check_permission(user_id: int):
        # check user
        user = await UserRepository.find_one_by_id(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng không tồn tại!")

        return user.is_admin
