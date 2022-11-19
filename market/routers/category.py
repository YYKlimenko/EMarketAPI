from typing import Any

from fastapi import APIRouter, Depends

from market.schemas import Category, CreatingCategory
from market.objects import PERMIT_FOR_ADMIN
from market.services import CategoryService

router = APIRouter(tags=['Categories'])


@router.get(
    '/categories/',
    status_code=200,
    description='Get the categories',
)
async def get_categories(name: str | None = None, service=Depends(CategoryService)):
    return await service.retrieve_list(name=name)


@router.get(
    '/categories/{id}',
    status_code=200,
    description='Get the category',
)
async def get_category(category_id: int, service=Depends(CategoryService)) -> Category:
    return await service.retrieve_by_id(category_id)


@router.post(
    '/categories/',
    status_code=201,
    description='Create a new category',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def post_category(category: CreatingCategory, service=Depends(CategoryService)) -> None:
    return await service.create(category)


@router.put(
    '/categories/{id}',
    status_code=202,
    description='The category is updated',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_category(
        data: dict[str, Any], category_id: int, service=Depends(CategoryService)
) -> None:
    return await service.update(data, category_id)


@router.delete(
    '/categories/{id}',
    status_code=202,
    description='The category is deleted',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_category(category_id: int, service=Depends(CategoryService)) -> None:
    return await service.delete(category_id)
