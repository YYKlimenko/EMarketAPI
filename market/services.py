from datetime import datetime

from bcrypt import gensalt, hashpw
from fastapi import UploadFile, Form, Depends, Path, HTTPException
from pydantic import Field
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.dataclasses import SignFloat
from core.settings import db
from core.services.services import Service
from market.utils.image_edit import ImageFileUploader, ImageFileDeleter
from market.schemas import (
    CreatingCategory, Category, Product, CreatingProduct, Image, CreatingImage,
    CreatingOrder, Order, CreatingUser, User
)


class CategoryService(Service):
    async def create(self, instance: CreatingCategory, session: AsyncSession = db) -> None:
        return await super()._create(instance, session)

    async def retrieve_list(self, session: AsyncSession = db, name: str | None = None):
        return await super()._retrieve_list(session, name=name)


class ProductService(Service):
    class SignPrice(SignFloat):
        sign_value: str | None = Field(default=None, alias='price')

    async def create(self, instance: CreatingProduct, session: AsyncSession = db) -> None:
        return await super()._create(instance, session)

    async def retrieve_list(
            self,
            session: AsyncSession = db,
            name: str | None = None,
            price: str | None = Depends(SignPrice),
            category_id: int | None = None
    ) -> list[Row]:
        return await super()._retrieve_list(
            session, name=name, price=price, category_id=category_id
        )


class ImageService(Service):

    async def create_image(
            self,
            file: UploadFile,
            product_id: int = Form(),
            session: AsyncSession = db
    ) -> None:
        url = await ImageFileUploader(file, str(product_id)).upload()
        image = {'url': url, 'product_id': product_id}
        try:
            await self._repository.create(self._model, image, session)
        except IntegrityError:
            await ImageFileDeleter('media', url).delete()

    async def delete_image(self, image_id: int, session: AsyncSession = db) -> None:
        if image := await self.retrieve_by_id(image_id, session=session):
            await ImageFileDeleter('media', image.url).delete()
            return await self.delete(image_id, session=session)

    async def retrieve_list(
            self, session: AsyncSession = db, product_id: int | None = None
    ) -> list[Row]:
        return await super()._retrieve_list(session, product_id=product_id)


class UserService(Service):

    async def registrate(self, user: CreatingUser, session: AsyncSession = db) -> None:
        user = {'username': user.username,
                'number': user.number,
                'hashed_password': hashpw(user.password.encode(), gensalt()),
                'is_admin': False,
                'date_registration': datetime.utcnow()}
        return await self._repository.create(self._model, user, session)

    async def retrieve_list(
            self, session: AsyncSession = db, username: str | None = None, number: str | None = None
    ) -> list[Row]:
        return await super()._retrieve_list(session, username=username, number=number)


class OrderService(Service):

    async def create(self, order: CreatingOrder, session: AsyncSession = db) -> None:
        products = await self._repository.get_relations(Product, order.products_id, session)
        if len(products) == 0:
            raise HTTPException(422)
        await self._repository.create(self._model, {**order.dict(), 'products': products}, session)

    # async def retrieve_by_id(self, _id: int = Path(alias='id'), session: AsyncSession = db) -> Row:
    #     order = await self._repository.retrieve(self._model, self._fields, session, id=(_id, '=='))
    #     products = await self._repository.retrieve(
    #         ProductOrder, [ProductOrder.product_id, ], session, True, order_id=(_id, '==')
    #     )
    #     return self._creating_model(**order, products_id=[product[0] for product in products])

    # async def retrieve_list(self, session: AsyncSession = db) -> list[Row]:
    #     query = select(self._model, Product.id).outerjoin(self._model.products)
    #     orders_products = await session.execute(query.order_by(self._model.id))
    #     orders = {}
    #     for order_product in orders_products:
    #         order = order_product[0].dict()
    #         if orders.get(order['id']):
    #             orders[order['id']]['products_id'].add(order_product[1])
    #         else:
    #             order['products_id'] = {order_product[1]}
    #             orders[order['id']] = order
    #     return list(orders.values())
