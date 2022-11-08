from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from auth.services.interfaces import AuthorizationRepository


class SQLAuthorizationRepository(AuthorizationRepository):

    def __init__(self, model: declarative_base()):
        self.model: declarative_base() = model

    async def get_auth_data(
            self, field: str, value: Any, session: AsyncSession, password_field: str = 'password'
    ) -> dict[str, str | int]:
        query = select(getattr(self.model, 'id'), getattr(self.model, password_field))
        data = (await session.execute(query.where(getattr(self.model, field) == value))).all()[0]
        return {'id': data[0], 'password': data[1]}
