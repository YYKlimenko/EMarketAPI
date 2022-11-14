from fastapi import APIRouter, Depends

from core.permissions.permissions import PERMIT_FOR_ADMIN
from market.schemas import Product
from market.objects import product_service as service


router = APIRouter(tags=['Products'])


@router.get(
    '/products/',
    status_code=200,
    description='Get the product',
)
async def get_products(response=Depends(service.retrieve_list)) -> list[Product]:
    return response


@router.get(
    '/products/{id}',
    status_code=200,
    description='Get the products',
)
async def get_product(response=Depends(service.retrieve_by_id)) -> Product:
    return response


@router.post(
    '/products/',
    status_code=201,
    description='Create a new product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def post_product(response=Depends(service.create)) -> None:
    return response


@router.put(
    '/products/{id}',
    status_code=202,
    description='Update the product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_product(response=Depends(service.update)) -> Product:
    return response


@router.delete(
    '/products/{id}',
    status_code=202,
    description='Delete the product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_product(response=Depends(service.delete)) -> Product:
    return response
