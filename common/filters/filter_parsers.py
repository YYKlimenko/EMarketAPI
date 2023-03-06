"""Filter parser classes."""

__all__ = ['FilterParser', 'FloatFilterParser', 'IntFilterParser']

import operator
from abc import ABC
from http.client import HTTPException
from typing import Callable, Any

from common.filters import Filter


class FilterParser(ABC):
    """The class to create Filter from string objects in format like {sign}_{value}.

    It is an abstract class.
    cls._type variable define type of value in creating a Filter class.
    The child types must redefine cls._type variable.
    """

    _type: Any

    @classmethod
    def parse(cls, raw_string: str | None = None) -> Filter[Any]:
        """Parse string, create and return a Filter object.

        Arguments:
        raw_string --- string object must be in format like {sign}_{value}. For example: eq_100.

        Exceptions:
        HTTPException(422) --- in case the string (raw_data) is incorrect.
        """
        if raw_string:
            raw_data = raw_string.split('_')
            if len(raw_data) != 2:
                raise HTTPException(422)
            sign, value = cls._convert_type(raw_data)
            return Filter[cls._type](sign=sign, value=value)  # type: ignore

    @classmethod
    def _convert_type(cls, raw_data: list[str]) -> tuple[Callable[..., bool], object]:
        """To validate and convert types for creating a Filter valid object.

        Arguments:
        raw_data --- a list object is contains two str objects (sign equivalent, value).

        Exceptions:
        HTTPException(422) --- in case the sign or the value is incorrect.
        """
        try:
            sign = getattr(operator, raw_data[0])
            value = cls._type(raw_data[1])
        except ValueError:
            raise HTTPException(422, 'Invalid types')
        return sign, value


class FloatFilterParser(FilterParser):
    """The class parse string in a Filter object which the value has float type."""

    _type: type = float


class IntFilterParser(FilterParser):
    """The class parse string in a Filter object which the value has int type."""

    _type: type = int
