from typing import List

from fastapi import HTTPException, status

from app.core import db
from app.models import Order, OrderItem
from app.models.Order import OrderStatus
from app.repositories import OrderRepository, ProductRepository, OrderItemRepository
from app.schemas import OrderSchema, ChangeOrderStatusSchema


class OrderService:

    @staticmethod
    async def get_all():
        objects = await OrderRepository.find_all()
        new_objects = []
        for obj in objects:
            new_objects.append(obj.to_dict(relationships=["buyer", "order_items"]))
        return new_objects

    @staticmethod
    async def get_list_by_buyer_id(buyer_id: int):
        objects = await OrderRepository.find_list_by_buyer_id(buyer_id=buyer_id)
        new_objects = []
        for obj in objects:
            new_objects.append(obj.to_dict(relationships=["buyer", "order_items"]))
        return new_objects

    @staticmethod
    async def get_one_by_id(id: int):
        # check order
        order = await OrderRepository.find_one_by_id(id=id)

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đơn hàng!")

        return order.to_dict(relationships=["buyer", "order_items"])

    @staticmethod
    async def add_one(schema: OrderSchema, buyer_id: int):
        # check product and quantity
        for order_item in schema.order_items:
            product = await ProductRepository.find_one_by_id(id=order_item.product_id)
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Không tìm thấy sản phẩm!")

            if product.quantity < order_item.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Số lượng sản phẩm không hợp lệ!")

        try:
            # create order
            total_price = 0
            total_quantity = 0
            for order_item in schema.order_items:
                total_price += order_item.price
                total_quantity += order_item.quantity

            new_order = Order(
                address=schema.address,
                phone_number=schema.phone_number,
                total_price=total_price,
                total_quantity=total_quantity,
                buyer_id=buyer_id,
            )

            created_order = await OrderRepository.create_one(new_model=new_order, in_transaction=True)

            # create order item
            new_order_items = []
            for order_item in schema.order_items:
                new_order_item = OrderItem(
                    product_id=order_item.product_id,
                    price=order_item.price,
                    quantity=order_item.quantity,
                    order_id=created_order.id
                )
                new_order_items.append(new_order_item)

            created_order.order_items = await OrderItemRepository.create_list(new_models=new_order_items,
                                                                              in_transaction=True)

            # change quantity product
            for order_item in created_order.order_items:
                product = await ProductRepository.find_one_by_id(id=order_item.product_id)
                await ProductRepository.change_quantity(id=order_item.product_id,
                                                        new_quantity=product.quantity - order_item.quantity,
                                                        in_transaction=True)

            await db.commit()
            return created_order.to_dict(relationships=["buyer", "order_items"])
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Lỗi máy chủ: {e}")

    @staticmethod
    async def change_status(id: int, schema: ChangeOrderStatusSchema):
        # check order
        order = await OrderRepository.find_one_by_id(id=id)

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đơn hàng!")

        if order.status == schema.status.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Trạng thái đơn hàng không hợp lệ!")

        if order.status != OrderStatus.CANCELLED.value and schema.status.value != OrderStatus.CANCELLED.value:
            await OrderRepository.change_status(id=order.id, status=schema.status.value)
            return

        if order.status == OrderStatus.CANCELLED.value and schema.status.value != OrderStatus.CANCELLED.value:
            try:
                for order_item in order.order_items:
                    product = await ProductRepository.find_one_by_id(id=order_item.product_id)
                    await ProductRepository.change_quantity(id=order_item.product_id,
                                                            new_quantity=product.quantity - order_item.quantity,
                                                            in_transaction=True)
                await OrderRepository.change_status(id=order.id, status=schema.status.value, in_transaction=True)
                await db.commit()
                return
            except Exception as e:
                await db.rollback()
                raise ValueError(f"Lỗi máy chủ: {e}")

        if order.status != OrderStatus.CANCELLED.value and schema.status.value == OrderStatus.CANCELLED.value:
            try:
                for order_item in order.order_items:
                    product = await ProductRepository.find_one_by_id(id=order_item.product_id)
                    await ProductRepository.change_quantity(id=order_item.product_id,
                                                            new_quantity=product.quantity + order_item.quantity,
                                                            in_transaction=True)
                await OrderRepository.change_status(id=order.id, status=schema.status.value, in_transaction=True)
                await db.commit()
                return
            except Exception as e:
                await db.rollback()
                raise ValueError(f"Lỗi máy chủ: {e}")

    @staticmethod
    async def remove_one(id: int):
        try:
            order = await OrderRepository.find_one_by_id(id=id)

            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Không tìm thấy đơn hàng!")

            if order.status != OrderStatus.CANCELLED.value and order.status != OrderStatus.COMPLETED.value:
                for order_item in order.order_items:
                    product = await ProductRepository.find_one_by_id(id=order_item.product_id)
                    await ProductRepository.change_quantity(id=order_item.product_id,
                                                            new_quantity=product.quantity + order_item.quantity,
                                                            in_transaction=True)

            remove_count = await OrderRepository.delete_one(id=id, in_transaction=True)
            await db.commit()
            return remove_count
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Lỗi máy chủ: {e}")

    @staticmethod
    async def remove_list(ids: List[int]):
        try:
            for id in ids:
                order = await OrderRepository.find_one_by_id(id=id)

                if not order:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Không tìm thấy đơn hàng!")

                if order.status != OrderStatus.CANCELLED.value and order.status != OrderStatus.COMPLETED.value:
                    for order_item in order.order_items:
                        product = await ProductRepository.find_one_by_id(id=order_item.product_id)
                        await ProductRepository.change_quantity(id=order_item.product_id,
                                                                new_quantity=product.quantity + order_item.quantity,
                                                                in_transaction=True)

            remove_count = await OrderRepository.delete_list(ids=ids, in_transaction=True)
            await db.commit()
            return remove_count
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Lỗi máy chủ: {e}")