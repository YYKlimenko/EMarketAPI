from fastapi import APIRouter, Depends

from auth.objects import authenticator
from core.settings import repository
from market.models import ProductCategory, CreatingProductCategory
from market.services import CategoryService

router = APIRouter(tags=['Categories'])
service = CategoryService(repository, ProductCategory, CreatingProductCategory)


@router.get('/categories/')
async def get_categories(response=Depends(service.retrieve_list)) -> list[ProductCategory]:
    return response


@router.get('/categories/{id}')
async def get_category(response=Depends(service.retrieve_by_id)) -> ProductCategory:
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
