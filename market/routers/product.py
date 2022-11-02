from fastapi import APIRouter, Depends

from auth.objects import authenticator
from core.repositories import SQLAsyncRepository
from market.models import ProductModel
from market.services import ProductService
from market.schemas import Product, CreatingProduct


router = APIRouter(tags=['Products'])
repository = SQLAsyncRepository(ProductModel)
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
