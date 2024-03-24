import requests
from fastapi import APIRouter, status, Security, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.core import get_settings
from app.repositories import JWTBearer
from app.schemas import ResponseSchema, ProcessPaymentSchema
from app.services import PaymentService, AuthService, UserService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/payment", tags=["Payment"])


@router.get("", response_model=ResponseSchema)
async def get_all_payment(request: Request, user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "payment",
            "method": request.method,
            "action": "get all",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await PaymentService.get_all()
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy tất cả thanh toán thành công", result=result)


@router.get("/{id}", response_model=ResponseSchema)
async def get_one_payment_by_id(id: int, request: Request,
                                user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "payment",
            "method": request.method,
            "action": "get one",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await PaymentService.get_one_by_id(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin thanh toán thành công", result=result)


@router.post("/{id}", response_model=ResponseSchema)
async def process_payment(id: int, request: Request, request_body: ProcessPaymentSchema,
                          user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "payment",
            "method": request.method,
            "action": "process payment",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    await PaymentService.process_payment(id=id, schema=request_body)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thanh toán đơn hàng thành công")
