from typing import Protocol, Any

from pydantic import BaseModel
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from market.models import TableModel as Model


class RepositoryInterface(Protocol):

    async def create(self, fields: dict[str, Any], session: AsyncSession) -> None:
        raise NotImplementedError

    async def retrieve(
            self, data: BaseModel, session: AsyncSession, many: bool = False, **kwargs
    ) -> Row | list[Row]:
        raise NotImplementedError

    async def update(self, _id: int, data: dict[str, Any], session: AsyncSession) -> None:
        raise NotImplementedError

    async def delete(self, _id, session: AsyncSession):
        raise NotImplementedError

    # @staticmethod
    # async def get_relations(relation: Model, foreign_key: Any, session: AsyncSession) -> list[Row]:
    #     raise NotImplementedError

    async def get_filters(self, kws: dict[str, Any]) -> list:
        raise NotImplementedError

    @staticmethod
    async def commit(session: AsyncSession, query=None) -> None:
        raise NotImplementedError


