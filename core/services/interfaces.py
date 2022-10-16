from typing import Protocol
from sqlmodel import SQLModel


class RepositoryInterface(Protocol):
    async def create(self, model: type, instance: SQLModel) -> None:
        pass

    async def retrieve(self, model: type, field: str, value: str | int
                       ) -> SQLModel:
        pass

    async def retrieve_list(self, model: type, **kwargs) -> list[SQLModel]:
        pass

    async def edit(
            self, model: type, instance_id: int, data: SQLModel | None
    ) -> None:
        pass