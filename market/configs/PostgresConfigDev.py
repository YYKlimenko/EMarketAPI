"""The Development Config class for connecting to Postgres."""

from common.configs import AbstractSQLConfig  # type: ignore
from .PostgresConfig import PostgresConfig


class PostgresConfigDev(PostgresConfig):  # type: ignore
    """The Config class for connecting to Postgres."""

    DIALECT_DB: str = 'postgresql'
    DRIVER_DB: str = 'asyncpg'
    LOGIN_DB: str = 'postgres'
    PASSWORD_DB: str = 'Yura'
    HOST_DB: str = 'localhost'
    PORT_DB: int = 5432
    DB_NAME: str = 'market'
