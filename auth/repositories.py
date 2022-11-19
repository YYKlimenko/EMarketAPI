from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import declarative_base

from auth.settings import USER_MODEL
from market.configs.PostgresConfig import PostgresConfig


class SQLAuthorizationRepository:
    model: declarative_base() = USER_MODEL

    def __init__(self, db_config=Depends(PostgresConfig)):
        self.session_maker = db_config.get_session_maker()

    async def get_auth_data(
            self, field: str, value: Any, password_field: str = 'password'
    ) -> dict[str, str | int]:
        async with self.session_maker() as session:
            query = select(getattr(self.model, 'id'), getattr(self.model, password_field))
            data = (await session.execute(
                query.where(getattr(self.model, field) == value))
                    ).all()[0]
            return {'id': data[0], 'password': data[1]}
