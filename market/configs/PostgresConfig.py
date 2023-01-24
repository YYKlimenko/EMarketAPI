import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from common.configs.configs import Config


class PostgresConfig(Config):
    DIALECT_DB = 'postgresql'
    DRIVER_DB = 'asyncpg'
    LOGIN_DB = os.getenv('LOGIN_DB')
    PASSWORD_DB = os.getenv('PASSWORD_DB')
    HOST_DB = 'db'
    PORT_DB = 5432
    DB_NAME = 'market'
    URL_DB = f'{LOGIN_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{DB_NAME}'

    def get_engine(self):
        return create_async_engine(
            f'{self.DIALECT_DB}+{self.DRIVER_DB}://{self.get_url_db()}', future=True, echo=True
        )

    def get_session_maker(self):
        return sessionmaker(self.get_engine(), expire_on_commit=False, class_=AsyncSession)

    @staticmethod
    def get_url_db():
        self = PostgresConfig
        return f'{self.LOGIN_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.DB_NAME}'
