from enum import Enum
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, validator


class SignEnum(str, Enum):
    eq = '=='
    lt = '<'
    gt = '>'
    le = '<='
    ge = '>='


class SignValue(BaseModel):
    _sign_dict = {'eq': '==', 'lt': '<', 'gt': '>', 'le': '<=', 'ge': '>='}
    sign_value: str | None

    @staticmethod
    def _check_type(value: str) -> Any:
        pass

    @validator('sign_value')
    def validate(cls, sign_value: str | None):
        if sign_value is None:
            cls.sign, cls.value = None, None
        else:
            sign_value = sign_value.split('_')
            if len(sign_value) != 2:
                raise HTTPException(422)
            try:
                cls.sign = cls._sign_dict[sign_value[0]]
                cls.value = cls._check_type(sign_value[1])
            except ValueError:
                raise HTTPException(422, 'Invalid types')


class SignFloat(SignValue):
    @staticmethod
    def _check_type(value):
        return float(value)
