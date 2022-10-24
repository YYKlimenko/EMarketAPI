from typing import Any

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.engine import Row
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class SQLAsyncRepository:

    def __init__(self, model: type, response_model: type | None) -> None:
        self._model: type = model
        self._response_model: type = response_model

    async def _get_response_fields(self) -> list[Row]:
        return [getattr(self._model, field) for field in self._response_model.__fields__.keys()]

    async def _get_select(self) -> Any:
        return select(*await self._get_response_fields()
                      ) if self._response_model else select(self._model)

    async def _filter_query(self, query, **kwargs):
        for _ in await self._get_filters(kwargs):
            query = query.where(_)
        return query

    async def _retrieve(self, instances) -> SQLModel | None:
        if len(instances):
            return self._response_model(**instances[0]) if self._response_model else instances[0]

    async def _retrieve_list(self, instances) -> list[SQLModel]:
        return instances.all() if self._response_model else instances.scalars().all()

    async def _update(self, instance_id, data: dict[str, Any]) -> None:
        return update(self._model).where(self._model.id == instance_id).values(**data)

    async def _delete(self, instance_id):
        return delete(self._model).where(self._model.id == instance_id)

    async def create_from_dict(self, data: dict[str, Any], session: AsyncSession) -> None:
        session.add(self._model(**data))
        return await session.commit()

    async def create(self, instance: SQLModel, session: AsyncSession) -> None:
        return await self.create_from_dict(instance.dict(), session)

    async def retrieve(self, session: AsyncSession, many: bool = False, **kwargs):
        query = await self._get_select()
        if kwargs:
            query = await self._filter_query(query, **kwargs)
        instances = await session.execute(query)
        instances = instances.all() if self._response_model else instances.scalars().all()
        return instances if many else await self._retrieve(instances)

    async def edit(
            self, instance_id: int, session: AsyncSession, data: dict[str, Any] | None
    ) -> None:
        query = self._update(instance_id, data) if data else self._delete(instance_id)
        await session.execute(await query)
        return await session.commit()

    async def _get_filters(self, kwargs: dict) -> list:
        filters: list = []
        for key in kwargs:
            if isinstance(kwargs[key], tuple):
                left_condition, right_condition = getattr(self._model, key), kwargs[key][0]
                match kwargs[key][1]:
                    case 'gt': filters.append(left_condition > right_condition)
                    case 'ge': filters.append(left_condition >= right_condition)
                    case 'lt': filters.append(left_condition < right_condition)
                    case 'le': filters.append(left_condition <= right_condition)
                    case 'eq': filters.append(left_condition == right_condition)
                    case _: raise HTTPException(422, detail='The sign is not correct')
        return filters
