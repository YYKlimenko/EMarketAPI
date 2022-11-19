from os import getenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from market.models import UserModel

DEBUG = True

SECRET_KEY = 'KYKOYAKO'
USER_MODEL = UserModel
SUPERUSERS = {1}

"""Настройка подключения к SQL-БД"""
if DEBUG:
    LOGIN_DB = 'postgres'
    PASSWORD_DB = 'YuraMarketPassword___1984'
else:
    LOGIN_DB = getenv('LOGIN_DB')
    PASSWORD_DB = getenv('PASSWORD_DB')

DIALECT_DB = 'postgresql'
DRIVER_DB = 'asyncpg'
URL_DB = f'{LOGIN_DB}:{PASSWORD_DB}@localhost:5432/market'
URL_TEST_DB = f'{LOGIN_DB}:{PASSWORD_DB}@localhost:5432/test_market'

engine = create_async_engine(
    f'{DIALECT_DB}+{DRIVER_DB}://{URL_DB}', future=True, echo=True
)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
