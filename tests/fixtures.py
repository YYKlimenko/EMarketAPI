import logging

import pytest

from auth.configs import AuthConfig, AuthConfigDev
from main import app
from market.configs.MediaConfig import MediaConfig
from market.configs.PostgresConfig import PostgresConfig
from tests.client import client
from tests.configs import PostgresConfigTestDev
from tests.configs.MediaConfigTest import MediaConfigTest
from tests.scripts import create_tables


@pytest.fixture(scope='session')
def set_test_environment():
    create_tables(PostgresConfigTestDev)
    app.dependency_overrides[PostgresConfig] = PostgresConfigTestDev
    app.dependency_overrides[MediaConfig] = MediaConfigTest
    app.dependency_overrides[AuthConfig] = AuthConfigDev


@pytest.fixture(scope='session')
def get_admin_header():
    response = client.post(
        "/authentication/", json={'login': 'admin', 'password': 'admin'}
    )
    return f"Bearer {response.json()['access_token']}"


@pytest.fixture(scope='session')
def get_user_header():
    token = client.post(
        "/authentication/", json={'login': 'user', 'password': 'user'}
    )
    return f"Bearer {token.json()['access_token']}"
