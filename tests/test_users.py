from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.repositories import SQLAsyncRepository
from core.settings import URL_TEST_DB
from main import app
from market.schemas import CreatingUser, User
from market.services import UserService
from market.models import (  # noqa: F401
    CategoryModel, ProductModel, UserModel, OrderModel,
    ProductOrderLink, ImageModel, TableModel
)

client = TestClient(app)

SUPERUSER_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' \
                  'eyJleHAiOjE2Njg4NzgyNzksImlhdCI6MTY2ODgzNTA3OS' \
                  'wic3ViIjoxfQ.oR3CJ6MaAR1uxx22vcdAJNeltMKzAlZB_jX0cHdcRfc'


def create_database_data():
    engine = create_engine(f'postgresql+psycopg2://{URL_TEST_DB}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
    return engine


def set_user_repository():
    engine = create_database_data()
    session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    user_repository = SQLAsyncRepository(UserModel, session_maker)
    UserService(user_repository, CreatingUser, User, ['number', 'username'])

    # app.dependency_overrides[service.retrieve_list] = override_get_db


def test_get_users():
    response = client.get("/users/", headers={'Authorization': SUPERUSER_TOKEN})
    assert response.status_code == 200
