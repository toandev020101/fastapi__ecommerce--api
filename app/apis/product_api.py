from fastapi import APIRouter, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core import get_settings
from app.repositories import JWTBearer
from app.schemas import ResponseSchema, ProductSchema, RemoveSchema
from app.services import AuthService, ProductService

settings = get_settings()

router = APIRouter(prefix=f"{settings.BASE_API_SLUG}/product", tags=["Product"])


@router.get("", response_model=ResponseSchema)
async def get_all_product():
    result = await ProductService.get_all()
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy tất cả sản phẩm thành công", result=result)


@router.get("/{id}", response_model=ResponseSchema)
async def get_one_product_by_id(id: int):
    result = await ProductService.get_one_by_id(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Lấy thông tin sản phẩm thành công", result=result)


@router.post("", response_model=ResponseSchema)
async def add_one_product(request_body: ProductSchema,
                          user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await ProductService.add_one(schema=request_body, creator_id=user_id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Thêm sản phẩm thành công", result=result)


@router.put("/{id}", response_model=ResponseSchema)
async def update_one_product(id: int, request_body: ProductSchema,
                             user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await ProductService.update_one(id=id, schema=request_body)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Cập nhật sản phẩm thành công", result=result)


@router.delete("/{id}", response_model=ResponseSchema)
async def remove_one_product(id: int,
                             user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await ProductService.remove_one(id=id)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa sản phẩm thành công", result=result)


@router.delete("", response_model=ResponseSchema)
async def remove_list_product(request_body: RemoveSchema,
                              user_decode: HTTPAuthorizationCredentials = Security(JWTBearer())):
    user_id = user_decode.get("user_id")

    check_permission = await AuthService.check_permission(user_id=user_id)
    if not check_permission:
        return ResponseSchema(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện yêu cầu này!",
                              result=None)

    result = await ProductService.remove_list(ids=request_body.ids)
    return ResponseSchema(status_code=status.HTTP_200_OK, detail="Xóa danh sách sản phẩm thành công", result=result)
