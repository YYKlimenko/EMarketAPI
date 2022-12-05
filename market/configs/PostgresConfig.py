from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import LOGIN_DB, PASSWORD_DB
from market.configs.Config import Config


class PostgresConfig(Config):
    DIALECT_DB = 'postgresql'
    DRIVER_DB = 'asyncpg'
    URL_DB = f'{LOGIN_DB}:{PASSWORD_DB}@db:5432/market'
    URL_TEST_DB = f'{LOGIN_DB}:{PASSWORD_DB}@db:5432/test_market'

    def get_engine(self):
        return create_async_engine(
            f'{self.DIALECT_DB}+{self.DRIVER_DB}://{self.URL_DB}', future=True, echo=True
        )

    def get_session_maker(self):
        return sessionmaker(self.get_engine(), expire_on_commit=False, class_=AsyncSession)
