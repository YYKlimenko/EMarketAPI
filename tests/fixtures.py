from datetime import datetime

import pytest
from bcrypt import hashpw, gensalt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.settings import URL_TEST_DB
from main import app
from market.configs.PostgresConfig import PostgresConfig
from market.models import TableModel, UserModel
from tests.client import client
from tests.configs.PostgresConfigTest import PostgresConfigTest


def create_test_data(engine):

    with Session(engine) as session:
        users = [
            UserModel(
                username='admin',
                number='89006772323',
                password=hashpw('admin'.encode(), gensalt()).decode(),
                date_registration=datetime.utcnow(),
                is_admin=True),
            UserModel(
                username='user',
                number='89006005588',
                password=hashpw('user'.encode(), gensalt()).decode(),
                date_registration=datetime.utcnow(),
                is_admin=False
            )
        ]
        session.add_all(users)
        session.commit()


def create_tables():
    engine = create_engine(f'postgresql+psycopg2://{URL_TEST_DB}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
    create_test_data(engine)


def override_dependencies():
    app.dependency_overrides[PostgresConfig] = PostgresConfigTest


@pytest.fixture(scope='session')
def set_test_environment():
    create_tables()
    override_dependencies()


@pytest.fixture(scope='session')
def get_admin_header(scope='session'):
    token = client.post(
        "/authentication/", json={'login': 'admin', 'password': 'admin'}
    )
    return f"Bearer {token.json()['access_token']}"


@pytest.fixture(scope='session')
def get_user_header(scope='session'):
    token = client.post(
        "/authentication/", json={'login': 'user', 'password': 'user'}
    )
    return f"Bearer {token.json()['access_token']}"
