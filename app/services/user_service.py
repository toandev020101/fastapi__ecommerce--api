from fastapi import HTTPException, status

from app.repositories import PaymentRepository, UserRepository


class UserService:

    @staticmethod
    async def get_one_by_id(id: int):
        # check user
        user = await UserRepository.find_one_by_id(id=id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy người dùng!")

        return user.to_dict()
