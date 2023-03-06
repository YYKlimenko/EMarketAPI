"""Pydantic schemas for User model."""

__all__ = ['BaseUserSchema', 'CreatingUserSchema', 'RetrievingUserSchema', 'UpdatingUserSchema']

from datetime import datetime
import string

from bcrypt import hashpw, gensalt
from pydantic.class_validators import validator
from pydantic.fields import Field

from .base_schemas import BaseSchema, ID


class BaseUserSchema(BaseSchema):
    """Base user schema schema."""

    username: str = Field(max_length=30, default='username')
    number: str = Field(max_length=12, default='89050965588')


class CreatingUserSchema(BaseUserSchema):
    """Pydantic schema to create User instance in DB."""

    password: str = Field(max_length=256, default='password')
    password2: str = Field(max_length=256, default='password')

    @validator('password')
    def match_passwords(cls, password: str, values: dict[str, str]) -> str:
        """Validate passwords."""
        password2 = values.get('password2')
        if password2 and password2 != password:
            raise ValueError('Passwords don\'t match')
        else:
            del password2
            hashed_password = hashpw(password.encode(), gensalt()).decode(),
            del password
            return hashed_password[0]

    @validator('number')
    def check_number(cls, number: str, values: dict[str, str]) -> str:
        """Validate cellphone number."""
        begin = 1 if number[0] == '+' else 0
        length = 12 if number[0] == '+' else 11
        if len(number) == length:
            for n in number[begin:]:
                if n not in string.digits:
                    break
            else:
                return number
        raise ValueError('Telephone number is not correct')


class RetrievingUserSchema(BaseUserSchema, ID):
    """Pydantic schema to get User instance from DB."""

    date_registration: datetime = datetime.utcnow()
    is_admin: bool = False


class UpdatingUserSchema(BaseSchema):
    """Pydantic schema to update User instance in DB."""

    username: str | None = Field(max_length=30, default=None)
    number: str | None = Field(max_length=12, default=None)
