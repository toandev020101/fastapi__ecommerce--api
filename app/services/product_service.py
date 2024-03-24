from typing import List

from fastapi import HTTPException, status

from app.models import Product
from app.schemas import ProductSchema
from app.repositories import ProductRepository


class ProductService:

    @staticmethod
    async def get_all():
        objects = await ProductRepository.find_all()
        new_objects = []
        for obj in objects:
            new_objects.append(obj.to_dict())
        return new_objects

    @staticmethod
    async def get_one_by_id(id: int):
        # check product
        product = await ProductRepository.find_one_by_id(id=id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy sản phẩm!")

        return product.to_dict()

    @staticmethod
    async def add_one(schema: ProductSchema, creator_id: int):
        # check product
        product = await ProductRepository.find_one_by_name(name=schema.name)

        if product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tên sản phẩm đã tồn tại!")

        new_product = Product(
            name=schema.name,
            description=schema.description,
            price=schema.price,
            quantity=schema.quantity,
            creator_id=creator_id
        )
        created_product = await ProductRepository.create_one(new_model=new_product)
        return created_product.to_dict()

    @staticmethod
    async def update_one(id: int, schema: ProductSchema):
        # check product
        product = await ProductRepository.find_one_by_id(id=id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy sản phẩm!")

        # check name
        if schema.name != product.name:
            product = await ProductRepository.find_one_by_name(name=schema.name)
            if product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Tên sản phẩm đã tồn tại!")

        new_product = product
        new_product.name = schema.name
        new_product.description = schema.description
        new_product.price = schema.price
        new_product.quantity = schema.quantity
        updated_product = await ProductRepository.update_one(id=id, new_model=new_product)
        return updated_product.to_dict()

    @staticmethod
    async def remove_one(id: int):
        remove_count = await ProductRepository.delete_one(id=id)
        if remove_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy sản phẩm!")
        return remove_count

    @staticmethod
    async def remove_list(ids: List[int]):
        remove_count = await ProductRepository.delete_list(ids=ids)
        if remove_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy sản phẩm!")
        return remove_count
