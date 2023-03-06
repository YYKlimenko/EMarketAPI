"""The module include Abstract types to create config types."""

from abc import ABC

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore


__all__ = ['AbstractConfig', 'AbstractSQLConfig']


class AbstractConfig(ABC):
    """Abstract class for creating config types."""

    ...


class AbstractSQLConfig(AbstractConfig):
    """Abstract class for creating config types to connect to DB through SQLAlchemy."""

    DIALECT_DB: str
    DRIVER_DB: str
    LOGIN_DB: str
    PASSWORD_DB: str
    HOST_DB: str
    PORT_DB: int
    DB_NAME: str

    def get_engine(self) -> AsyncEngine:
        """Get async engine for connecting to DB."""
        return create_async_engine(
            f'{self.DIALECT_DB}+{self.DRIVER_DB}://{self.get_url_db()}', future=True, echo=True
        )

    def get_session_maker(self) -> sessionmaker:
        """Get session maker to create session for connecting to DB."""
        return sessionmaker(self.get_engine(), expire_on_commit=False, class_=AsyncSession)

    def get_url_db(self) -> str:
        """Get url for connecting to DB."""
        return f'{self.LOGIN_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.DB_NAME}'
