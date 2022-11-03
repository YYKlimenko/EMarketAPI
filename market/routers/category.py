from fastapi import APIRouter, Depends

from core.repositories import SQLAsyncRepository
from market.schemas import Category, CreatingCategory
from market.services import CategoryService
from market.models import CategoryModel


router = APIRouter(tags=['Categories'])
repository = SQLAsyncRepository(CategoryModel)
service = CategoryService(repository, CreatingCategory, Category)


@router.get('/categories/')
async def get_categories(response=Depends(service.retrieve_list)) -> list[Category]:
    return response


@router.get('/categories/{id}')
async def get_category(response=Depends(service.retrieve_by_id)) -> Category:
    return response


@router.post('/categories/')
async def post_category(response=Depends(service.create)) -> None:
    return response


@router.put('/categories/{id}')
async def put_category(response=Depends(service.update)) -> None:
    return response


@router.delete('/categories/{id}')
async def delete_category(response=Depends(service.delete)) -> None:
    return response
