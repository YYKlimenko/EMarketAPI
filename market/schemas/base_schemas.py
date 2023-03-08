"""Base schemas to create other schemas."""

__all__ = ['BaseSchema', 'BaseUpdatingSchema', 'ID']

from pydantic import root_validator, ValidationError
from pydantic.main import BaseModel


class BaseSchema(BaseModel):
    """The base schema class to create all other schemas."""

    class Config:
        orm_mode = True


class ID(BaseModel):
    """The id field. """

    id: int


class BaseUpdatingSchema(BaseSchema):

    @root_validator
    def is_not_empty(cls, values):
        if any(values.values()):
            return values
        raise ValidationError('The schema can\'t be empty')

