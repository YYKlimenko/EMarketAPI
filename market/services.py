from datetime import datetime
from typing import AsyncGenerator

from bcrypt import gensalt, hashpw
from fastapi import UploadFile, Form, Depends, HTTPException, Path
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel

from auth.models import CreatingUser, User, RetrievingUser
from core.services.dataclasses import SignFloat
from core.settings import get_async_session as ASYNC_SESSION
from core.services.services import Service, RelativeService
from market.utils.image_edit import ImageFileUploader, ImageFileDeleter
from market.models import (
    CreatingProductCategory, ProductCategory, Product, CreatingProduct, Image, CreatingImage,
    # CreatingOrder, Order, NewOrder
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
    _response_model: type | None = RetrievingUser
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
            session.add(user)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                422,
                detail='Username and number must be unique'
            )

    async def change_data(
            self,
            user_id: int,
            username: str | None = None,
            number: str | None = None,
            session: AsyncGenerator = Depends(ASYNC_SESSION)
    ) -> None:
        data = {}
        for attribute in ('username', 'number'):
            if locals().get(attribute):
                data[attribute] = locals().get(attribute)
        instance = update(self._model).where(self._model.id == user_id)
        instance = instance.values(**data)
        await session.execute(instance)
        await session.commit()


# class OrderService(RelativeService):
#     _model: type = Order
#     _creating_model: type = CreatingOrder
#     _filter_kwargs: dict[str, type] = {'user_id': int}
#     _back_relative_fields: dict[str, type] = {'user_id': User}
#
#     async def create(
#             self,
#             order: NewOrder,
#             session: AsyncGenerator = Depends(ASYNC_SESSION)
#     ) -> SQLModel:
#         print('Hello')
#         # products = []
#         # for i in order.products_id:
#         #     product =
#         # # order = await self.repository.retrieve(
#         # #     self._model, self._response_model, 'id', instance_id, session
#         # # )
#         # # products = await order.products
