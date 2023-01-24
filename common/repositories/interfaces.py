from typing import Any

from pydantic import BaseModel

from market.configs import Config


class CRUDRepositoryInterface:

    def __init__(self, config: Config) -> None:
        raise NotImplementedError

    async def create(self, fields: dict[str, Any]) -> None:
        raise NotImplementedError

    async def retrieve(self, data: BaseModel, many: bool = False, **kwargs) -> Any:
        raise NotImplementedError

    async def update(self, _id: int, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def delete(self, _id):
        raise NotImplementedError
