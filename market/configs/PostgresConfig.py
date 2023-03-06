"""The Config class for connecting to Postgres."""

import os

from common.configs import AbstractSQLConfig  # type: ignore


class PostgresConfig(AbstractSQLConfig):  # type: ignore
    """The Config class for connecting to Postgres."""

    DIALECT_DB: str = 'postgresql'
    DRIVER_DB: str = 'asyncpg'
    LOGIN_DB: str = os.getenv('LOGIN_DB')
    PASSWORD_DB: str = os.getenv('PASSWORD_DB')
    HOST_DB: str = 'db'
    PORT_DB: int = 5432
    DB_NAME: str = 'market'
