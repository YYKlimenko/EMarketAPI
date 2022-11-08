from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories import SQLAsyncRepository


class OrderAsyncPostgresRepository(SQLAsyncRepository):

    async def get_products(
            self, relation: str, foreign_keys: list[int], session: AsyncSession
    ) -> list[Row]:
        relation = self.relations[relation]
        query = select(relation).where(relation.id.in_(foreign_keys))
        return (await session.execute(query)).scalars().all()

    async def retrieve_with_products(
            self, session: AsyncSession, many: bool = False, **kwargs
    ) -> Row | list[Row]:
        raw_query = f"""SELECT order_id, user_id, product_id, name, 
                     description, constitution, price, category_id
                     FROM orders 
                     JOIN product_order_link ON orders.id = product_order_link.order_id 
                     JOIN products ON products.id = product_order_link.product_id""" # noqa W291
        if many:
            if kwargs.get('user_id'):
                filter_by_user_id = f"""WHERE user_id = {kwargs['user_id']}"""
                raw_query = ' '.join([raw_query, filter_by_user_id, ';'])
        else:
            filter_by_id = f"""WHERE order_id = {kwargs['_id']}"""  # noqa W291
            raw_query = ' '.join([raw_query, filter_by_id])
        return await session.execute(raw_query)
