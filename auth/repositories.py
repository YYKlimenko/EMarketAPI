from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import declarative_base as sql_model

from market.configs.PostgresConfig import PostgresConfig


class SQLAuthorizationRepository:

    def __init__(self, db_config=Depends(PostgresConfig)):
        self.session_maker = db_config.get_session_maker()

    async def get_auth_data(
            self, field: str, value: Any, model: sql_model(), password_field: str = 'password'
    ) -> dict[str, str | int]:
        async with self.session_maker() as session:
            query = select(getattr(model, 'id'), getattr(model, password_field))
            try:
                data = (await session.execute(
                    query.where(getattr(model, field) == value))
                        ).all()[0]
                return {'id': data[0], 'password': data[1]}
            except IndexError:
                raise HTTPException(422, 'The User is not exists')
