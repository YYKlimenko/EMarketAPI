from datetime import datetime

from bcrypt import gensalt, hashpw
from fastapi import UploadFile, HTTPException, Path
from sqlalchemy.exc import IntegrityError

from core.services.metaclasses import ServiceMeta
from core.services.services import Service, DeleteUpdateMixin
from market.dataclasses import SignPrice
from market.repositories import (
    CategoryRepository, ImageRepository, ProductRepository, UserRepository, OrderRepository
)
from market.utils.image_edit import ImageEditor
from market.schemas import (
    CreatingCategory, CreatingProduct, CreatingOrder, CreatingUser, Order, Product, Category,
    Image, CreatingImage, User
)


class CategoryService(Service):
    creating_schema = CreatingCategory
    response_schema = Category
    repository = CategoryRepository


class ProductService(Service):
    creating_schema = CreatingProduct
    response_schema = Product
    repository = ProductRepository

    async def retrieve_list(
            self, name: str | None, price: SignPrice | None, category_id: int | None
    ) -> list[Product]:
        price = (price.sign, price.value) if price.sign and price.value else None
        raw_products = await self.repository.retrieve_with_images(
            many=True, name=name, price=price, category_id=category_id
        )

        products = {}
        for row in raw_products:
            if row.product_id not in products:
                products[row.product_id] = Product(
                        id=row.product_id,
                        name=row.name,
                        description=row.description,
                        constitution=row.constitution,
                        price=row.price,
                        category_id=row.category_id,
                        images=[]
                )
            if row.image_id:
                products[row.product_id].images.append({'id': row.image_id, 'url': row.url})

        return list(products.values())

    async def retrieve_by_id(
            self,
            _id: int = Path(alias='id')
    ) -> Product | None:
        raw_product = await self.repository.retrieve_with_images(_id=_id)
        product = None

        for n, row in enumerate(raw_product):
            if n == 0:
                product = Product(
                        id=row.product_id,
                        name=row.name,
                        description=row.description,
                        constitution=row.constitution,
                        price=row.price,
                        category_id=row.category_id,
                        images=[]
                )

            if row.image_id:
                product.images.append({'id': row.image_id, 'url': row.url})

        return product


class ImageService(Service):
    creating_schema = CreatingImage
    response_schema = Image
    repository = ImageRepository

    async def create_image(
            self, file: UploadFile, product_id: int, image_editor: ImageEditor
    ) -> None:
        url = await image_editor.upload(file, str(product_id))
        image = {'url': url, 'product_id': product_id}
        try:
            await self.repository.create(image)
        except IntegrityError:
            await image_editor.delete(url)

    async def delete_image(self, image_id: int, image_editor: ImageEditor) -> None:
        if image := await self.retrieve_by_id(image_id):
            await image_editor.delete(image.url)
            return await self.delete(image_id)


class UserService(Service):
    creating_schema = CreatingUser
    response_schema = User
    repository = UserRepository
    updatable_fields = ['username']

    async def registrate(self, user: CreatingUser) -> None:
        user = {'username': user.username,
                'number': user.number,
                'password': hashpw(user.password.encode(), gensalt()).decode(),
                'is_admin': False,
                'date_registration': datetime.utcnow()}
        try:
            return await self.repository.create(user)
        except IntegrityError:
            raise HTTPException(422, 'The username or the number already registered')


class OrderService(Service):
    creating_schema = CreatingUser
    response_schema = User
    repository = OrderRepository
    updatable_fields = []

    async def create(self, instance: CreatingOrder) -> None:
        products = await self.repository.get_products(instance.products)
        if len(products) == 0:
            raise HTTPException(422)
        instance_data = instance.dict()
        instance_data.pop('products')
        instance_data['products'] = products
        return await self.repository.create(instance_data)

    async def retrieve_by_id(
            self, _id: int = Path(alias='id')
    ) -> Order | None:
        order_product = await self.repository.retrieve_with_products(_id=_id)
        order = None
        products = {}
        for row in order_product:
            if order is None:
                order = Order(id=row.order_id, user_id=row.user_id, products={})

            if row.product_id not in products:
                products[row.product_id] = Product(
                    id=row.product_id,
                    name=row.name,
                    description=row.description,
                    constitution=row.constitution,
                    price=row.price,
                    category_id=row.category_id,
                    images=[]
                )

            if row.image_id:
                products[row.product_id].images.append({'id': row.image_id, 'url': row.url})

        if order:
            order.products = list(products.values())
        return order

    async def retrieve_list(
            self, user_id: int | None = None
    ) -> list[Order]:
        order_product = await self.repository.retrieve_with_products(
            many=True, user_id=user_id
        )
        orders = {}
        for row in order_product:

            if row.order_id not in orders:
                orders[row.order_id] = Order(id=row.order_id, user_id=row.user_id, products={})

            if row.product_id not in orders[row.order_id].products:
                orders[row.order_id].products[row.product_id] = Product(
                    id=row.product_id,
                    name=row.name,
                    description=row.description,
                    constitution=row.constitution,
                    price=row.price,
                    category_id=row.category_id,
                    images=[]
                )

            if row.image_id:
                orders[row.order_id].products[row.product_id].images.append(
                    {'id': row.image_id, 'url': row.url}
                )

        for order in orders:
            orders[order].products = list(orders[order].products.values())

        return list(orders.values())
