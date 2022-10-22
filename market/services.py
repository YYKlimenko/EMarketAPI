from datetime import datetime
from typing import AsyncGenerator, Any

from bcrypt import gensalt, hashpw
from fastapi import UploadFile, Form, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel, select

from auth.models import CreatingUser, RetrievingUser, User
from core.services.dataclasses import SignFloat
from core.settings import get_async_session as ASYNC_SESSION
from core.services.services import Service, RelativeService
from market.utils.image_edit import ImageFileUploader, ImageFileDeleter
from market.models import (
    CreatingProductCategory, ProductCategory, Product, CreatingProduct, Image, CreatingImage,
    CreatingOrder, Order, ProductOrderLink
)


class CategoryService(Service):
    _creating_model = CreatingProductCategory
    _model = ProductCategory
    _filter_kwargs = {'name': str}


class ProductService(RelativeService):
    class SignPrice(SignFloat):
        sign_value: str | None = Field(default=None, alias='price')

    _creating_model = CreatingProduct
    _model = Product
    _back_relative_fields = {'category_id': ProductCategory}
    _filter_kwargs = {'name': str, 'price': SignPrice, 'category_id': int}


class ImageService(RelativeService):
    _model: type = Image
    _creating_model: type = CreatingImage
    _filter_kwargs: dict[str, type] = {'product_id': int}
    _back_relative_fields: dict[str, type] = {'product_id': Product}

    async def create_image(
            self,
            file: UploadFile,
            product_id: int = Form(..., alias='product_id'),
            session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> None:
        url = await ImageFileUploader(file, str(product_id)).upload()
        creating_image = self._creating_model(url=url, product_id=product_id)
        return await self.create(creating_image, session=session)

    async def delete_image(
            self, image_id: int, session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> None:
        if image := await self.retrieve_by_id(image_id, session=session):
            await ImageFileDeleter('media', image.url).delete()
            return await self.delete(image_id, session=session)


class UserService(Service):
    _model: type = User
    _creating_model: type = CreatingUser
    _response_model: type = RetrievingUser
    _final_fields = ['hashed_password', 'date_registration', 'is_admin']
    _filter_kwargs: dict[str, type] = {'username': str}

    async def registrate(
            self, user: _creating_model, session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> None:
        user = self._model(username=user.username,
                           number=user.number,
                           hashed_password=hashpw(user.password.encode(), gensalt()),
                           is_admin=False,
                           date_registration=datetime.utcnow())
        try:
            await self.create(instance=user, session=session)
        except IntegrityError:
            raise HTTPException(
                422,
                detail='Username and number must be unique'
            )


class OrderService(RelativeService):
    _model: type = Order
    _creating_model: type = CreatingOrder
    _filter_kwargs: dict[str, type] = {'user_id': int}
    _back_relative_fields: dict[str, type] = {'user_id': User}

    async def create(
            self,
            order: CreatingOrder,
            session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> None:
        products = (
            await session.execute(select(Product).where(Product.id.in_(order.products_id)))
        ).scalars().all()
        order = self._model(**order.dict(), products=products)
        session.add(order)
        await session.commit()

    async def retrieve_by_id(
            self,
            order_id: int = Path(..., alias='id'),
            session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> SQLModel:
        order = (
            await session.execute(select(self._model).where(self._model.id == order_id))
        ).scalar()
        products = (
            await session.execute(
                select(ProductOrderLink.product_id).where(ProductOrderLink.order_id == order_id)
            )
        ).scalars().all()
        return self._creating_model(**order.dict(), products_id=products)

    async def retrieve_list(
            self,
            session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> list:
        select_statement = select(self._model, Product.id).outerjoin(self._model.products)
        orders_products = await session.execute(select_statement.order_by(self._model.id))
        orders = {}
        while True:
            try:
                order_product = next(orders_products)
                order = order_product[0].dict()
                if orders.get(order['id']):
                    orders[order['id']]['products_id'].add(order_product[1])
                else:
                    order['products_id'] = {order_product[1]}
                    orders[order['id']] = order
            except StopIteration:
                break
        return list(orders.values())

