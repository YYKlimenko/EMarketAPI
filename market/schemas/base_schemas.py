"""Base schemas to create other schemas."""

__all__ = ['BaseSchema', 'ID']

from pydantic.main import BaseModel


class BaseSchema(BaseModel):
    """The base schema class to create all other schemas."""

    class Config:
        orm_mode = True


class ID(BaseModel):
    """The id field. """

    id: int
