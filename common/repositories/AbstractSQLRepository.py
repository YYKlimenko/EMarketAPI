"""The Repository Classes to work with databases."""
import abc
from typing import Any

from fastapi.exceptions import HTTPException
from sqlalchemy import delete, select, update  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore

from common.configs import AbstractSQLConfig  # type: ignore
from common.models import TableModel  # type: ignore
from common.filters import Filter


__all__ = ['AbstractSQLRepository']


class AbstractSQLRepository(abc.ABC):
    """The async repository class is based on SQLAlchemy."""

    __slots__ = ('session_maker',)

    model: TableModel

    def __init__(self, config: AbstractSQLConfig) -> None:
        """Init an SQL repository object.

        Arguments:
        config --- Config object to connect to a database.
        """
        self.session_maker: sessionmaker = config.get_session_maker()

    async def create(self, data: dict[str, Any]) -> None:
        """Create an instance in a database.

        Arguments:
        data --- columns (key: value) for creating an instance in a database.
        """
        async with self.session_maker() as session:
            session.add(self.model(**data))
            return await self.commit(session)

    async def retrieve(
            self,
            fields: list[str] | None = None,
            filter_fields: dict[str, Filter[Any] | Any] | None = None
    ) -> Any:
        """Retrieve an instance from a database.

        Arguments:
        fields --- columns are retrieved from a database,
        filter_fields --- these fields are used to create filter conditions.
        """
        async with self.session_maker() as session:
            query = select(
                *[getattr(self.model, attr) for attr in fields]
            ) if fields else select(self.model)
            if filter_fields:
                query = query.where(*await self.get_filter_expressions(**filter_fields))

            return [instance.__dict__ for instance in (await session.execute(query)).scalars().all()]

    async def update(self, instance_id: int, data: dict[str, Any]) -> None:
        """Update an instance in a database.

        Arguments:
        instance_id --- id of an updating instance,
        data --- columns (key: value) for updating an instance in a database.
        """
        async with self.session_maker() as session:
            query = update(self.model).where(self.model.id == instance_id).values(**data)
            return await self.commit(session, query)

    async def delete(self, instance_id: int) -> None:
        """Delete an instance in a database.

        Arguments:
        instance_id --- id of an deleting instance.
        """
        async with self.session_maker() as session:
            query = delete(self.model).where(self.model.id == instance_id)
            return await self.commit(session, query)

    async def get_filter_expressions(self, **filter_fields: Filter[Any] | Any) -> list[Any]:
        """Create filter SQLAlchemy-type expressions from SignValue objects."""
        filters = []
        for field in filter_fields:
            if isinstance(filter_fields[field], Filter):
                filter_ = filter_fields[field].sign(getattr(self.model, field), filter_fields[field].value)
            else:
                filter_ = getattr(self.model, field).__eq__(filter_fields[field])
            filters.append(filter_)
        return filters

    @staticmethod
    async def commit(session: AsyncSession, query: Any = None) -> None:
        """Execute sql-query and commit it.

        Exceptions:
        HTTPException --- in case an invalid query.
        """
        try:
            if query is not None:
                await session.execute(query)
            await session.commit()
        except IntegrityError as exception:
            print(exception)
            raise HTTPException(422, 'The query is incorrect') from exception
