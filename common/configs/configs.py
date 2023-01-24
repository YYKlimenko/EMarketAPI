import os


class Config:
    pass


class ConfigSecurity:
    SECRET_KEY = os.getenv('SECRET_KEY')
