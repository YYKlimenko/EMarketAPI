"""The Product Model endpoints."""

__all__ = ['product_router']

from typing import Any

from fastapi import APIRouter, Depends, Query

from common.permissions import permit_for_admin
from common.filters import FloatFilterParser

from common.functions import get_fields
from market.schemas import CreatingProductSchema, RetrievingProductSchema, UpdatingProductSchema
from market.services import ProductService

product_router = APIRouter(prefix='/products', tags=['Products'])


@product_router.get(
    '/',
    status_code=200,
    description='Get the list of products',
    response_model=list[RetrievingProductSchema],
)
async def get_products(
        price: str | None = None,
        category_id: int | None = None,
        service: ProductService = Depends(),
) -> list[dict[str, Any]]:
    return await service.retrieve(
        many=True,
        **get_fields(price=FloatFilterParser.parse(price), category_id=category_id)
    )


@product_router.get(
    '/{product_id}/',
    status_code=200,
    description='Get the product by id',
    response_model=RetrievingProductSchema | None,
)
async def get_product(product_id: int, service: ProductService = Depends()) -> dict[str, Any]:
    return await service.retrieve(**get_fields(id=product_id))


@product_router.post(
    '/',
    status_code=201,
    description='Create a new product',
    dependencies=[Depends(permit_for_admin)],
)
async def post_product(product: CreatingProductSchema, service: ProductService = Depends()) -> None:
    return await service.create(product.dict())


@product_router.put(
    '/{product_id}/',
    status_code=202,
    description='Update the product',
    dependencies=[Depends(permit_for_admin)],
)
async def put_product(product_id: int, product: UpdatingProductSchema, service: ProductService = Depends()) -> None:
    return await service.update(product_id, get_fields(**product.dict()))


@product_router.delete(
    '/{product_id}/',
    status_code=202,
    description='Delete the product',
    dependencies=[Depends(permit_for_admin)],
)
async def delete_product(product_id: int, service: ProductService = Depends()) -> None:
    return await service.delete(product_id)
