"""Repositories types to the market application."""

__all__ = [
    'ImageSQLRepository',
    'SQLRepository',
    'CategorySQLRepository',
    'ProductSQLRepository',
    'OrderSQLRepository',
    'UserSQLRepository'
]

from typing import Type, Any

from fastapi import Depends
from sqlalchemy import select

from common.filters import Filter
from common.repositories.AbstractSQLRepository import AbstractSQLRepository
from market.configs import PostgresConfig
from market.models import CategoryModel, ImageModel, OrderModel, ProductModel, UserModel, ProductOrderLink


class SQLRepository(AbstractSQLRepository):
    """Abstract repository with the config injection."""

    def __init__(self, config: PostgresConfig = Depends()) -> None:
        """Init repository instance."""
        super().__init__(config)


class CategorySQLRepository(SQLRepository):
    """Category model's repository."""

    model: Type[CategoryModel] = CategoryModel


class UserSQLRepository(SQLRepository):
    """User model's repository."""

    model: Type[UserModel] = UserModel


class ImageSQLRepository(SQLRepository):
    """Image model's repository."""

    model: Type[ImageModel] = ImageModel


class ProductSQLRepository(SQLRepository):
    """Product model's repository."""

    model: Type[ImageModel] = ProductModel

    async def retrieve(
            self,
            fields: list[str] | None = None,
            filter_fields: dict[str, Filter[Any] | Any] | None = None
    ) -> Any:
        raw_query = f"""SELECT product.id as product_id, product.name, product.description, 
                            product.constitution, product.price, product.category_id, 
                            image.id as image_id, image.url
                            FROM products as product 
                            LEFT JOIN images as image ON product.id = image.product_id """  # noqa W291

        if filter_fields:
            count_kwargs = 0
            filters = []

            for kwarg in ('id', 'category_id', 'price'):
                if filter_fields.get(kwarg) is not None:
                    word = 'WHERE' if count_kwargs == 0 else 'AND'

                    if kwarg == 'id':
                        filters.append(f"""{word} {kwarg} = '{filter_fields[kwarg]}'""")

                    elif kwarg == 'category_id':
                        filters.append(f"""{word} {kwarg} = {filter_fields[kwarg]}""")

                    elif kwarg == 'price':
                        symbol = '=' if filter_fields[kwarg][0] == '==' else filter_fields[kwarg][0]
                        filters.append(f"""{word} {kwarg} {symbol} {filter_fields[kwarg][1]}""")

                    count_kwargs += 1
            raw_query = ' '.join([raw_query, *filters, ';'])

        async with self.session_maker() as session:
            raw_products = await session.execute(raw_query)

        products = {}
        for row in raw_products:
            if row.product_id not in products:
                products[row.product_id] = {
                    'id': row.product_id,
                    'name': row.name,
                    'description': row.description,
                    'constitution': row.constitution,
                    'price': row.price,
                    'category_id': row.category_id,
                    'images': []
                }
            if row.image_id:
                products[row.product_id]['images'].append({'id': row.image_id, 'url': row.url})

        return list(products.values())


class OrderSQLRepository(SQLRepository):
    """Order model's repository."""

    model: Type[OrderModel] = OrderModel

    async def create(self, data: dict[str, Any]) -> None:
        """Create the order instance in DB."""

        async with self.session_maker() as session:
            data['products'] = list((
                await session.execute(
                    select(ProductModel).where(ProductModel.id.in_(data['products']))
                )
            ).scalars())
            order = self.model(**data)
            session.add(order)
            return await self.commit(session=session)

    async def retrieve(
            self,
            fields: list[str] | None = None,
            filter_fields: dict[str, Filter[Any] | Any] | None = None
    ) -> Any:

        async with self.session_maker() as session:
            query = """
            SELECT orders.id, orders.user_id, 
            products.id as product_id, products.name, products.description, 
            products.price, products.category_id, products.constitution
            FROM orders 
            JOIN product_order_link ON orders.id = product_order_link.order_id
            JOIN products ON products.id = product_order_link.product_id 
            """
            for field in ('user_id', 'id'):
                if i := filter_fields.get(field):
                    query = ''.join([query, f' WHERE orders.{field} = {i}'])
            orders = dict()
            rows = await session.execute(query)
            for row in rows:
                if row.id not in orders:
                    orders[row.id] = {
                        'id': row.id,
                        'user_id': row.user_id,
                        'products': []
                    }
                orders[row.id]['products'].append(
                    {
                        'id': row.product_id,
                        'name': row.name,
                        'description': row.description,
                        'constitution': row.constitution,
                        'price': row.price,
                        'category_id': row.category_id,
                    }
                )
            return list(orders.values())
