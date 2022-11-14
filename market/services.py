from datetime import datetime

from bcrypt import gensalt, hashpw
from fastapi import UploadFile, Form, Depends, HTTPException, Path
from pydantic import Field
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.permissions.permissions import permit_for_admin
from core.services.dataclasses import SignFloat
from core.settings import db
from core.services.services import Service, DeleteUpdateMixin
from market.repositories import OrderAsyncPostgresRepository
from market.utils.image_edit import ImageFileUploader, ImageFileDeleter
from market.schemas import CreatingCategory, CreatingProduct, CreatingOrder, CreatingUser, Order, \
    Product


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
            await self._repository.create(image, session)
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
                'password': hashpw(user.password.encode(), gensalt()).decode(),
                'is_admin': False,
                'date_registration': datetime.utcnow()}
        return await self._repository.create(user, session)

    async def retrieve_list(
            self, session: AsyncSession = db, username: str | None = None, number: str | None = None
    ) -> list[Row]:
        return await super()._retrieve_list(session, username=username, number=number)


class OrderService(DeleteUpdateMixin):

    def __init__(self, repository: OrderAsyncPostgresRepository, updatable_fields: list[str]):
        self._repository = repository
        self._updatable_fields = updatable_fields

    async def create(self, instance: CreatingOrder, session: AsyncSession = db) -> None:
        products = await self._repository.get_products('product', instance.products, session)
        if len(products) == 0:
            raise HTTPException(422)
        instance_data = instance.dict()
        instance_data.pop('products')
        instance_data['products'] = products
        return await self._repository.create(instance_data, session)

    async def retrieve_by_id(
            self, _id: int = Path(alias='id'), session: AsyncSession = db
    ) -> Order:
        order_product = await self._repository.retrieve_with_products(session, _id=_id)
        order = None
        for row in order_product:
            if order is None:
                order = Order(id=row.order_id, user_id=row.user_id, products=[])
            order.products.append(
                Product(
                    id=row.product_id,
                    name=row.name,
                    description=row.description,
                    constitution=row.constitution,
                    price=row.price,
                    category_id=row.category_id
                )
            )
        return order

    async def retrieve_list(
            self, session: AsyncSession = db, user_id: int | None = None
    ) -> list[Order]:
        order_product = await self._repository.retrieve_with_products(
            session, many=True, user_id=user_id
        )
        orders = {}
        for row in order_product:
            if row.order_id not in orders:
                orders[row.order_id] = Order(
                    id=row.order_id,
                    user_id=row.user_id,
                    products=[]
                )
            orders[row.order_id].products.append(
                Product(
                        id=row.product_id,
                        name=row.name,
                        description=row.description,
                        constitution=row.constitution,
                        price=row.price,
                        category_id=row.category_id
                )
            )
        return list(orders.values())
