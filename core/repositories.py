from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.engine import Row
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class FilterQueriesCreator:

    @staticmethod
    async def get(kwargs: dict, model: type) -> list:
        _filter_queries: list = []
        for key in kwargs:
            match kwargs[key][1]:
                case 'gt': term = getattr(model, key) > kwargs[key][0]
                case 'ge': term = getattr(model, key) >= kwargs[key][0]
                case 'lt': term = getattr(model, key) < kwargs[key][0]
                case 'le': term = getattr(model, key) <= kwargs[key][0]
                case 'eq': term = getattr(model, key) == kwargs[key][0]
                case _: raise HTTPException(
                    422, detail='The sign is not correct')
            _filter_queries.append(term)
        return _filter_queries


class SQLAsyncRepository:
    _filter_queries_creator: FilterQueriesCreator = FilterQueriesCreator()

    @staticmethod
    async def _get_fields(model: type, response_model: type) -> list[Row]:
        return [getattr(model, field) for field in response_model.__fields__.keys()]

    async def create(self, model: type, instance: SQLModel, session: AsyncSession) -> None:
        session.add(model(**instance.dict()))
        await session.commit()

    async def retrieve(
            self,
            model: type,
            response_model: type | None,
            field: str,
            value: str | int,
            session: AsyncSession
    ) -> SQLModel | None:
        query = select(
            *await self.__class__._get_fields(model, response_model)
        ) if response_model else select(model)
        query = query.where(getattr(model, field) == value)
        instances = await session.execute(query)
        instances = instances.all() if response_model else instances.scalars().all()
        if not len(instances):
            return None
        else:
            return response_model(**instances[0]) if response_model else instances[0]

    async def retrieve_list(
            self,
            model: type,
            session: AsyncSession,
            response_model: type | None = None,
            **kwargs
    ) -> list[SQLModel]:
        query = select(
            *await self.__class__._get_fields(model, response_model)
        ) if response_model else select(model)
        if not kwargs:
            instances = await session.execute(query)
            return instances.all() if response_model else instances.scalars().all()
        else:
            filter_queries = await self._filter_queries_creator.get(kwargs, model)
            for filter_query in filter_queries:
                query = query.where(filter_query)
            instances = await session.execute(query)
        return instances.all() if response_model else instances.scalars().all()

    async def edit(self, model: type, instance_id: int, session: AsyncSession, data: SQLModel | None) -> None:
        if data:
            instance = update(model).where(model.id == instance_id)
            instance = instance.values(**data.dict())
        else:
            instance = delete(model).where(model.id == instance_id)
        await session.execute(instance)
        await session.commit()
