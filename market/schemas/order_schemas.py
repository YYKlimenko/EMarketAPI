"""Pydantic schemas for Order model."""

__all__ = ['CreatingOrderSchema', 'RetrievingOrderSchema']

from . import RetrievingProductSchema
from .base_schemas import BaseSchema, ID
from .product_schemas import BaseRetrievingProductSchema


class CreatingOrderSchema(BaseSchema):
    """Pydantic schema to create the Order instance in DB."""

    user_id: int
    products: list[int]


class RetrievingOrderSchema(ID):
    """Pydantic schema to get the Order instance from DB."""
    user_id: int
    products: list[BaseRetrievingProductSchema]
