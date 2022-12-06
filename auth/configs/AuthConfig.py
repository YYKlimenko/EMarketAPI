import os

from core.configs import Config
from market.models import UserModel


class AuthConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    USER_MODEL = UserModel
