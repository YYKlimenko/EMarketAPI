"""Pydantic schemas for Category model."""

__all__ = ['CreatingCategorySchema', 'RetrievingCategorySchema']

from pydantic.fields import Field

from .base_schemas import BaseSchema, ID


class CreatingCategorySchema(BaseSchema):
    """Pydantic schema to get data for creating a Category's instance."""

    name: str = Field(max_length=60)


class RetrievingCategorySchema(CreatingCategorySchema, ID):
    """Pydantic schema to get data from DB."""

    ...
