from typing import Any, AsyncGenerator

from fastapi import HTTPException, Path, Depends, Body
from pydantic import BaseModel, create_model
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.dataclasses import SignValue
from core.services.interfaces import RepositoryInterface
from core.services.utils import func_copy
from core.settings import get_async_session
from market.models import TableModel as Model


db = Depends(get_async_session)


class Service:

    def __init__(
            self,
            repository: RepositoryInterface,
            creating_model: Model,
            response_model: Model | None = None,
            updatable_fields: list[Any] | None = None,
            filters: dict[str, Any] | None = None
    ) -> None:
        self._repository = repository
        self._creating_schema = creating_model
        self._response_schema = response_model
        self._updatable_fields = updatable_fields or [
            attr for attr in self._response_schema.__fields__ if attr != 'id'
        ]

        self.filters = filters or dict()
        for key in self.filters:
            if issubclass(filters[key], SignValue):
                self.filters[key] = (Any, Depends(filters[key]))
            else:
                self.filters[key] = (filters[key] | None, None)

    async def _create(self, instance: BaseModel, session: AsyncSession):
        try:
            return await self._repository.create(instance.dict(), session)
        except IntegrityError:
            return None

    async def retrieve_by_id(self, _id: int = Path(alias='id'), session: AsyncSession = db) -> Row:
        return await self._repository.retrieve(self._response_schema, session, id=(_id, '=='))

    async def _retrieve_list(self, session: AsyncSession, **kwargs) -> list[Row]:
        for kwarg in kwargs:
            if isinstance(kwargs[kwarg], SignValue):
                kwargs[kwarg] = (kwargs[kwarg].value, kwargs[kwarg].sign)
            else:
                kwargs[kwarg] = (kwargs[kwarg], '==')
        kwargs = {key: kwargs[key] for key in kwargs if kwargs[key][0] is not None}
        return await self._repository.retrieve(self._response_schema, session, True, **kwargs)

    async def update(
            self, data: dict[str, Any], _id: int = Path(alias='id'), session: AsyncSession = db
    ) -> None:
        for key in data:
            if key not in self._updatable_fields:
                raise HTTPException(422)
        return await self._repository.update(_id, data, session)

    async def delete(self, _id: int = Path(alias='id'), session: AsyncSession = db) -> None:
        return await self._repository.delete(_id, session)
