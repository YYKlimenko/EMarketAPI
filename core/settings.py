from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# from auth.models import User
from repositories import SQLAsyncRepository


SECRET_KEY = 'KYKOYAKO'
# USER_MODEL = User

"""Настройка подключения к SQL-БД"""
# LOGIN_DB = getenv('LOGIN_DB')
# PASSWORD_DB = getenv('PASSWORD_DB')
LOGIN_DB = 'postgres'
PASSWORD_DB = 'YuraMarketPassword___1984'
DIALECT_DB = 'postgresql'
DRIVER_DB = 'asyncpg'
URL_DB = f'{LOGIN_DB}:{PASSWORD_DB}@localhost:5432/market'

engine = create_async_engine(
    f'{DIALECT_DB}+{DRIVER_DB}://{URL_DB}', future=True, echo=True
)
session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
repository_class = SQLAsyncRepository


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        yield db
