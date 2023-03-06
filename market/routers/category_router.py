"""The Category Model endpoints."""

__all__ = ['category_router']

from typing import Any

from fastapi import APIRouter, Depends

from auth.permissions import permit_for_admin  # type: ignore
from common.filters import Filter  # type: ignore
from market.schemas import RetrievingCategorySchema, CreatingCategorySchema  # type: ignore
from market.services import CategoryService


category_router = APIRouter(prefix='/categories', tags=['Categories'])


@category_router.get(
    '/',
    status_code=200,
    description='Get the categories',
    response_model=list[RetrievingCategorySchema],
)
async def get_categories(service: CategoryService = Depends()) -> list[dict[str, Any]]:
    return await service.retrieve(many=True)


@category_router.get(
    '/{category_id}/',
    status_code=200,
    description='Get the category',
    response_model=RetrievingCategorySchema | None,
)
async def get_category(category_id: int, service: CategoryService = Depends()) -> dict[str, Any]:
    result = await service.retrieve(id=category_id)
    return result


@category_router.post(
    '/',
    status_code=201,
    description='Create a new category',
    # dependencies=[Depends(permit_for_admin)]
)
async def post_category(category: CreatingCategorySchema, service: CategoryService = Depends()) -> None:
    return await service.create(category.dict())


@category_router.put(
    '/{category_id}/',
    status_code=202,
    description='The category is updated',
    # dependencies=[Depends(permit_for_admin)]
)
async def put_category(
        category: CreatingCategorySchema, category_id: int, service: CategoryService = Depends()
) -> None:
    return await service.update(category_id, category.dict())


@category_router.delete(
    '/{category_id}/',
    status_code=202,
    description='The category is deleted',
    # dependencies=[Depends(permit_for_admin)]
)
async def delete_category(category_id: int, service: CategoryService = Depends()) -> None:
    return await service.delete(category_id)
