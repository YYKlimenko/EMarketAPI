from typing import Protocol, Any

from sqlalchemy.engine import Row
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.main import SQLModelMetaclass as Model


class RepositoryInterface(Protocol):

    @staticmethod
    async def create(table: Model, fields: dict[str, Any], session: AsyncSession) -> None:
        raise NotImplementedError

    @staticmethod
    async def retrieve(
            model: Model, fields: list[Any], session: AsyncSession, many: bool = False, **kwargs
    ) -> Row | list[Row]:
        raise NotImplementedError

    @staticmethod
    async def update(model: Model, _id: int, data: dict[str, Any], session: AsyncSession) -> None:
        raise NotImplementedError

    @staticmethod
    async def delete(model: Model, _id, session: AsyncSession):
        raise NotImplementedError

    @staticmethod
    async def get_relations(relation: Model, foreign_key: Any, session: AsyncSession) -> list[Row]:
        raise NotImplementedError

    @staticmethod
    async def get_filters(model: Model, kws: dict[str, Any]) -> list:
        raise NotImplementedError

    @staticmethod
    async def commit(session: AsyncSession, query=None) -> None:
        raise NotImplementedError
