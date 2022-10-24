from typing import Any, AsyncGenerator

from fastapi import HTTPException, Path, Depends
from pydantic import BaseModel, create_model
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.services.dataclasses import SignValue
from core.services.interfaces import RepositoryInterface
from core.settings import get_async_session as ASYNC_SESSION


class ExistChecker:
    def __init__(self, repository: RepositoryInterface) -> None:
        self._repository = repository

    async def check(self, model: type, instance_id: int, session: AsyncSession) -> bool:
        return True if await self._repository.retrieve(
            model, None, 'id', instance_id, session) else False


class ServiceMeta(type):

    @classmethod
    def add_attributes(mcs, instance, attributes, dct):
        for attribute in attributes:
            if dct.get(attribute.__name__) is None:
                setattr(instance, attribute.__name__, attribute)

    def __new__(mcs, name, bases, dct):
        class_instance = super().__new__(mcs, name, bases, dct)
        _creating_model = dct.get('_creating_model', BaseModel)
        _model = dct.get('_model', BaseModel)
        class_instance._response_model = dct.get('_response_model', None)
        class_instance._final_fields = dct.get('_final_fields', [])

        def __init__(
                self,
                repository_class: type,
                model: type = _model,
                response_model: type = class_instance._response_model
        ) -> None:
            self.repository: RepositoryInterface = repository_class(model, response_model)

        async def create(
                self, instance: _creating_model, session: AsyncGenerator = Depends(ASYNC_SESSION)
        ) -> None:
            return await self.repository.create(instance, session)

        async def retrieve_by_id(
                self,
                instance_id: int = Path(..., alias='id'),
                session: AsyncGenerator = Depends(ASYNC_SESSION)
        ) -> SQLModel:
            return await self.repository.retrieve(session, id=(instance_id, 'eq'))

        async def update(
                self,
                data: dict[str, Any],
                instance_id: int = Path(..., alias='id'),
                session: AsyncGenerator = Depends(ASYNC_SESSION)
        ) -> None:
            for attr in data:
                if attr in self._final_fields or attr not in self._model.__fields__:
                    raise HTTPException(422, 'The attributes are not correct')
            return await self.repository.edit(instance_id, session, data=data)

        async def delete(
                self,
                instance_id: int = Path(..., alias='id'),
                session: AsyncGenerator = Depends(ASYNC_SESSION)
        ) -> None:
            return await self.repository.edit(instance_id, session, data=None)
        mcs.add_attributes(class_instance, (__init__, create, retrieve_by_id, update, delete), dct)

        return class_instance


class FilterServiceMeta(ServiceMeta):
    def __new__(mcs, name, bases, dct):
        class_instance = super().__new__(mcs, name, bases, dct)
        filter_kwargs = dct.get('_filter_kwargs', dict())
        for attribute in filter_kwargs:
            if issubclass(filter_kwargs[attribute], BaseModel):
                filter_kwargs[attribute] = (Any, Depends(filter_kwargs[attribute]))
            else:
                filter_kwargs[attribute] = (filter_kwargs[attribute] | None, None)

        filter_kwargs = create_model('FilterKwargs', **filter_kwargs)

        async def retrieve_list(
                self,
                session: AsyncGenerator = Depends(ASYNC_SESSION),
                kwargs: dict[str, type] = Depends(filter_kwargs),
        ) -> list[SQLModel]:
            if issubclass(kwargs.__class__, BaseModel):
                kwargs = kwargs.__dict__
            for kwarg in kwargs:
                if isinstance(kwargs[kwarg], SignValue):
                    kwargs[kwarg] = (kwargs[kwarg].value, kwargs[kwarg].sign)
                else:
                    kwargs[kwarg] = (kwargs[kwarg], 'eq')
            kwargs = {key: kwargs[key] for key in kwargs if kwargs[key][0]}
            return await self.repository.retrieve(session, many=True, **kwargs)

        mcs.add_attributes(class_instance, (retrieve_list, filter_kwargs), dct)
        return class_instance


class RelativeFilterServiceMeta(FilterServiceMeta):
    def __new__(mcs, name, bases, dct):
        class_instance = super().__new__(mcs, name, bases, dct)
        exist_checker = ExistChecker

        async def create(
                self,
                instance: dct.get('_creating_model', BaseModel),
                session: AsyncGenerator = Depends(ASYNC_SESSION)
        ) -> None:
            for field in self._back_relative_fields:
                _exist_checker = self.ExistChecker(self.repository)
                if not await _exist_checker.check(
                        self._back_relative_fields[field],
                        getattr(instance, field),
                        session
                ):
                    raise HTTPException(
                        422,
                        detail=f'{self._back_relative_fields[field].__name__} is not exists'
                    )
            return await self.repository.create(instance, session)

        mcs.add_attributes(class_instance, (create, exist_checker), dct)
        return class_instance


class Service(metaclass=FilterServiceMeta):
    pass


class RelativeService(metaclass=RelativeFilterServiceMeta):
    pass
