from fastapi import APIRouter, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core import get_settings
from app.repositories import JWTBearer
from app.schemas import ResponseSchema, ProcessPaymentSchema
from app.services import PaymentService, AuthService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/payment", tags=["Payment"])


@router.get("", response_model=ResponseSchema)
async def get_all_payment(user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await PaymentService.get_all()
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy tất cả thanh toán thành công", result=result)


@router.get("/{id}", response_model=ResponseSchema)
async def get_one_payment_by_id(id: int, user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await PaymentService.get_one_by_id(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin thanh toán thành công", result=result)


@router.post("/{id}", response_model=ResponseSchema)
async def process_payment(id: int, request_body: ProcessPaymentSchema):
    await PaymentService.process_payment(id=id, schema=request_body)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thanh toán đơn hàng thành công")
