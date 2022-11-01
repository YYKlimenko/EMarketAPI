from fastapi import APIRouter, Depends

from auth.objects import authenticator
from market.services import ProductService
from core.settings import repository
from market.models import Product, CreatingProduct


router = APIRouter(tags=['Products'])
service = ProductService(repository, Product, CreatingProduct)


@router.get('/products/')
async def get_products(response=Depends(service.retrieve_list)) -> list[Product]:
    return response


@router.get('/products/{id}')
async def get_product(response=Depends(service.retrieve_by_id)) -> Product:
    return response


@router.post('/products/')
async def post_product(response=Depends(service.create)) -> None:
    return response


@router.put('/products/{id}')
async def put_product(response=Depends(service.update)) -> Product:
    return response


@router.delete('/products/{id}')
async def delete_product(response=Depends(service.delete)) -> Product:
    return response
