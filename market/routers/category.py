from fastapi import APIRouter, Depends

from market.schemas import Category
from market.objects import category_service as service, PERMIT_FOR_ADMIN

router = APIRouter(tags=['Categories'])


@router.get(
    '/categories/',
    status_code=200,
    description='Get the categories',
)
async def get_categories(response=Depends(service.retrieve_list)) -> list[Category]:
    return response


@router.get(
    '/categories/{id}',
    status_code=200,
    description='Get the category',
)
async def get_category(response=Depends(service.retrieve_by_id)) -> Category:
    return response


@router.post(
    '/categories/',
    status_code=201,
    description='Create a new category',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def post_category(response=Depends(service.create)) -> None:
    return response


@router.put(
    '/categories/{id}',
    status_code=202,
    description='The category is updated',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_category(response=Depends(service.update)) -> None:
    return response


@router.delete(
    '/categories/{id}',
    status_code=202,
    description='The category is deleted',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_category(response=Depends(service.delete)) -> None:
    return response
