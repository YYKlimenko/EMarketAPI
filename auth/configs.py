"""The Config class for authorization and authentication."""

__all__ = ['AuthConfig', 'AuthConfigDev']

import os

from common.configs import AbstractConfig  # type: ignore
from market.models import UserModel  # type: ignore


class AuthConfig(AbstractConfig):
    """The Config class for authorization and authentication."""

    SECRET_KEY = os.getenv('SECRET_KEY')
    USER_MODEL = UserModel


class AuthConfigDev(AuthConfig):
    """The Development Config class for authorization and authentication."""

    SECRET_KEY = 'KEY'
