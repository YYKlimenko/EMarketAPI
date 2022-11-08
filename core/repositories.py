from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.interfaces import RepositoryInterface
from market.models import TableModel


class SQLAsyncRepository(RepositoryInterface):

    def __init__(self, model: TableModel, relations: dict[str, TableModel] | None = None) -> None:
        self.model: TableModel = model
        self.relations: dict[str, TableModel] | None = relations

    async def create(self, fields: dict[str, Any], session: AsyncSession) -> None:
        session.add(self.model(**fields))
        return await self.commit(session)

    async def retrieve(
            self, data: BaseModel, session: AsyncSession, many: bool = False, **kwargs
    ) -> Row | list[Row]:
        query = select(*[getattr(self.model, attr) for attr in data.__fields__])
        if kwargs:
            query = query.where(*await self.get_filters(kwargs))
        instances = await session.execute(query)
        return instances.all() if many else instances.first()

    async def update(self, _id: int, data: dict[str, Any], session: AsyncSession) -> None:
        try:
            query = update(self.model).where(self.model.id == _id).values(**data)
            return await self.commit(session, query)
        except IntegrityError:
            return None

    async def delete(self, _id, session: AsyncSession):
        query = delete(self.model).where(self.model.id == _id)
        return await SQLAsyncRepository.commit(session, query)

    async def get_filters(self, kws: dict[str, Any]) -> list:
        return [
            eval(f'm.{k} {kws[k][1]} kws[k][0]', {'m': self.model, 'kws': kws, 'k': k}) for k in kws
        ]

    @staticmethod
    async def commit(session: AsyncSession, query=None) -> None:
        if query is not None:
            await session.execute(query)
        return await session.commit()
