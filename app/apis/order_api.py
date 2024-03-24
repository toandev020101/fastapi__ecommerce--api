import requests
from fastapi import APIRouter, status, Security, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.core import get_settings
from app.repositories import JWTBearer
from app.schemas import ResponseSchema, RemoveSchema, OrderSchema, ChangeOrderStatusSchema
from app.services import OrderService, UserService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/order", tags=["Order"])


@router.get("", response_model=ResponseSchema)
async def get_all_order(request: Request, user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "get all",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await OrderService.get_all()
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy tất cả đơn hàng thành công", result=result)


@router.get("/list", response_model=ResponseSchema)
async def get_list_order_by_buyer_id(request: Request,
                                     user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "get list",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await OrderService.get_list_by_buyer_id(buyer_id=user_id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy danh sách đơn hàng thành công", result=result)


@router.get("/{id}", response_model=ResponseSchema)
async def get_one_order_by_id(id: int, user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await OrderService.get_one_by_id(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin đơn hàng thành công", result=result)


@router.post("", response_model=ResponseSchema)
async def add_one_order(request: Request, request_body: OrderSchema,
                        user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "add one",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await OrderService.add_one(schema=request_body, buyer_id=user_id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm đơn hàng thành công", result=result)


@router.patch("/{id}", response_model=ResponseSchema)
async def change_order_status(id: int, request: Request, request_body: ChangeOrderStatusSchema,
                              user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "change status",
            "is_admin": user.get("is_admin"),
            "status": request_body.status.value
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    await OrderService.change_status(id=id, schema=request_body)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Cập nhật trạng thái đơn hàng thành công")


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_one_order(id: int, request: Request,
                           user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "remove one",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await OrderService.remove_one(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa đơn hàng thành công", result=result)


@router.delete("", response_model=ResponseSchema)
async def remove_list_order(request: Request, request_body: RemoveSchema,
                            user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")
    user = await UserService.get_one_by_id(id=user_id)

    input_dict = {
        "input": {
            "path": "order",
            "method": request.method,
            "action": "remove list",
            "is_admin": user.get("is_admin")
        }
    }

    res = requests.post(settings.OPA_URL, json=input_dict)

    if not res.json().get("result").get("allow"):
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await OrderService.remove_list(ids=request_body.ids)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách đơn hàng thành công", result=result)
