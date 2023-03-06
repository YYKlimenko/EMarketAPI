"""The classes to create services."""

__all__ = ['AbstractService']

from typing import Any

from common.filters import Filter
from common.repositories import AbstractSQLRepository


class AbstractService:
    """The class to create services."""

    __slots__ = ('repository',)

    def __init__(self, repository: AbstractSQLRepository) -> None:
        """Init Service object."""
        self.repository = repository

    async def create(self, fields: dict[str, Any]) -> None:
        """Create a serviced object."""
        return await self.repository.create(fields)

    async def retrieve(
            self, many: bool = False, **filter_fields: Filter[Any] | Any
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """Retrieve a serviced object."""
        instances = await self.repository.retrieve(filter_fields=filter_fields)
        if many:
            return instances
        else:
            return instances[0] if len(instances) else None

    async def update(self, instance_id: int, data: dict[str, Any],) -> None:
        """Update a serviced object."""
        return await self.repository.update(instance_id, data)

    async def delete(self, instance_id: int) -> None:
        """Delete a serviced object."""
        return await self.repository.delete(instance_id)
