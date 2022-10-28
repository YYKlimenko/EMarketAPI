from typing import Any

from sqlalchemy import delete, select, update
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.main import SQLModelMetaclass as Model


class SQLAsyncRepository:

    @staticmethod
    async def create(table: Model, fields: dict[str, Any], session: AsyncSession) -> None:
        session.add(table(**fields))
        return await SQLAsyncRepository.commit(session)

    @staticmethod
    async def retrieve(model: dict, session: AsyncSession, many: bool = False, **kwargs):
        query = select(*model['fields'])
        if kwargs:
            query = query.where(*await SQLAsyncRepository.get_filters(model['table'], kwargs))
        instances = await session.execute(query)
        return instances.all() if many else instances.first()

    @staticmethod
    async def update(model: Model, _id: int, data: dict[str, Any], session: AsyncSession) -> None:

        query = update(model).where(model.id == _id).values(**data)
        return await SQLAsyncRepository.commit(session, query)

    @staticmethod
    async def delete(model: Model, _id, session: AsyncSession):
        query = delete(model).where(model.id == _id)
        return await SQLAsyncRepository.commit(session, query)

    @staticmethod
    async def get_filters(model: Model, kws: dict[str, Any]) -> list:
        print(kws)
        return [eval(f'm.{k} {kws[k][1]} kws[k][0]', {'m': model, 'kws': kws, 'k': k}) for k in kws]

    @staticmethod
    async def commit(session: AsyncSession, query=None) -> None:
        if query is not None:
            await session.execute(query)
        return await session.commit()
