"""Pydantic schemas for Product model."""

__all__ = ['CreatingProductSchema', 'RetrievingProductSchema', 'UpdatingProductSchema']

from pydantic import Field
from pydantic.types import Decimal

from . import BaseRetrievingImageSchema
from .base_schemas import BaseSchema, ID


class CreatingProductSchema(BaseSchema):
    """Pydantic schema to create Product instance in DB."""

    name: str = Field(max_lenght=60)
    description: str = Field(max_length=1000)
    constitution: str = Field(max_length=1000)
    price: Decimal
    category_id: int


class RetrievingProductSchema(CreatingProductSchema, ID):
    """Pydantic schema to get Product instance from DB."""
    images: list[BaseRetrievingImageSchema]


class UpdatingProductSchema(BaseSchema):
    name: str | None = Field(max_lenght=60, default=None)
    description: str = Field(max_length=1000, default=None)
    constitution: str = Field(max_length=1000, default=None)
    price: Decimal | None = Field(default=None)
    category_id: int | None = Field(default=None)
