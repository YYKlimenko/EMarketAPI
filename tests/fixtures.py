import pytest

from main import app
from market.configs.MediaConfig import MediaConfig
from market.configs.PostgresConfig import PostgresConfig
from tests.client import client
from tests.configs.MediaConfigTest import MediaConfigTest
from tests.configs.PostgresConfigTest import PostgresConfigTest
from tests.scripts import create_tables


@pytest.fixture(scope='session')
def set_test_environment():
    create_tables()
    app.dependency_overrides[PostgresConfig] = PostgresConfigTest
    app.dependency_overrides[MediaConfig] = MediaConfigTest


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
