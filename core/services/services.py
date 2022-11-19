from typing import Any

from fastapi import HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError

from core.services.dataclasses import SignValue
from market.models import TableModel as Model


class DeleteUpdateMixin:
    async def update(self, data: dict[str, Any], _id: int = Path(alias='id')) -> None:
        for key in data:
            if key not in self.updatable_fields:
                raise HTTPException(422)
        return await self.repository.update(_id, data)

    async def delete(self, _id: int = Path(alias='id')) -> None:
        return await self.repository.delete(_id)


class Service(DeleteUpdateMixin):
    creating_schema: Model | None = BaseModel
    response_schema: Model | None = BaseModel
    updatable_fields: list[Any] | None = [
            attr for attr in response_schema.__fields__ if attr != 'id'
        ]
    filters: dict[str, Any] = dict()

    def __init__(self, repository) -> None:
        self.repository = repository
        if not self.updatable_fields:
            self.updatable_fields: list[Any] | None = [
                attr for attr in self.response_schema.__fields__ if attr != 'id'
            ]

    async def create(self, instance: BaseModel):
        try:
            return await self.repository.create(instance.dict())
        except IntegrityError:
            return None

    async def retrieve_by_id(self, _id: int = Path(alias='id')) -> Row:
        return await self.repository.retrieve(self.response_schema, id=(_id, '=='))

    async def retrieve_list(self, **kwargs) -> list[Row]:
        for kwarg in kwargs:
            if isinstance(kwargs[kwarg], SignValue):
                kwargs[kwarg] = (kwargs[kwarg].value, kwargs[kwarg].sign)
            else:
                kwargs[kwarg] = (kwargs[kwarg], '==')
        kwargs = {key: kwargs[key] for key in kwargs if kwargs[key][0] is not None}
        return await self.repository.retrieve(self.response_schema, True, **kwargs)
