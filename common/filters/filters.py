"""Filter classes."""

__all__ = ['Filter']

import operator
from typing import Callable, Generic, TypeVar

from pydantic import BaseModel
from pydantic.class_validators import validator


T = TypeVar('T')


class Filter(BaseModel, Generic[T]):
    """The Filter class.

    The objects of the class contain value and sign to apply in filter expressions.
    Type of the value (T) is defined like Generic type.
    """
    value: T
    sign: Callable[..., bool] = operator.eq

    @validator('sign')
    def check_comparing_method(cls, sign: Callable[..., bool]) -> Callable[..., bool]:
        """To check that callable object enters in set of operator functions."""
        if sign not in {operator.eq, operator.lt, operator.le, operator.gt, operator.ge}:
            raise ValueError('The comparing method is incorrect')
        return sign
