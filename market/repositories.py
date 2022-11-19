from sqlalchemy import select
from sqlalchemy.engine import Row

import loggers
from core.repositories import SQLAsyncRepository
from market.models import ProductModel, OrderModel, CategoryModel, ImageModel, UserModel


class CategoryRepository(SQLAsyncRepository):
    model = CategoryModel


class ImageRepository(SQLAsyncRepository):
    model = ImageModel


class UserRepository(SQLAsyncRepository):
    model = UserModel


class OrderRepository(SQLAsyncRepository):
    model = OrderModel

    async def get_products(self, foreign_keys: list[int]) -> list[Row]:
        async with self.session_maker() as session:
            query = select(ProductModel).where(ProductModel.id.in_(foreign_keys))
            return (await session.execute(query)).scalars().all()

    async def retrieve_with_products(self, many: bool = False, **kwargs) -> Row | list[Row]:
        raw_query = f"""SELECT order_id, user_id, product_order_link.product_id, name, 
                     description, constitution, price, category_id, 
                     images.id as image_id, url
                     FROM orders 
                     JOIN product_order_link ON orders.id = product_order_link.order_id 
                     JOIN products ON products.id = product_order_link.product_id
                     LEFT JOIN images ON images.product_id = products.id
                    """ # noqa W291
        if many:
            if kwargs.get('user_id'):
                filter_by_user_id = f"""WHERE user_id = {kwargs['user_id']}"""
                raw_query = ' '.join([raw_query, filter_by_user_id, ';'])
        else:
            filter_by_id = f"""WHERE order_id = {kwargs['_id']}"""  # noqa W291
            raw_query = ' '.join([raw_query, filter_by_id])

        async with self.session_maker() as session:
            return await session.execute(raw_query)


class ProductRepository(SQLAsyncRepository):
    model = ProductModel

    async def retrieve_with_images(self, many: bool = False, **kwargs) -> Row | list[Row]:
        raw_query = f"""SELECT product.id as product_id, product.name, product.description, 
                     product.constitution, product.price, product.category_id, 
                     image.id as image_id, image.url
                     FROM products as product 
                     LEFT JOIN images as image ON product.id = image.product_id """ # noqa W291

        if many:

            count_kwargs = 0
            filters = []

            for kwarg in ('name', 'category_id', 'price'):
                if kwargs.get(kwarg) is not None:
                    word = 'WHERE' if count_kwargs == 0 else 'AND'

                    if kwarg == 'name':
                        filters.append(f"""{word} {kwarg} = '{kwargs[kwarg]}'""")

                    elif kwarg == 'category_id':
                        filters.append(f"""{word} {kwarg} = {kwargs[kwarg]}""")

                    elif kwarg == 'price':
                        symbol = '=' if kwargs[kwarg][0] == '==' else kwargs[kwarg][0]
                        filters.append(f"""{word} {kwarg} {symbol} {kwargs[kwarg][1]}""")

                    count_kwargs += 1


            raw_query = ' '.join([raw_query, *filters, ';'])
        else:
            filter_by_id = f"""WHERE product.id = {kwargs['_id']}"""  # noqa W291
            raw_query = ' '.join([raw_query, filter_by_id])

        async with self.session_maker() as session:
            return await session.execute(raw_query)
