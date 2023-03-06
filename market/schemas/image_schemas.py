"""Pydantic schemas for Image model."""

__all__ = ['BaseRetrievingImageSchema', 'RetrievingImageSchema']

from .base_schemas import BaseSchema, ID


class BaseRetrievingImageSchema(BaseSchema, ID):
    """Pydantic schema to view Image instance in Product schemas"""
    url: str


class RetrievingImageSchema(BaseRetrievingImageSchema):
    """Pydantic schema to view Image."""

    url: str

