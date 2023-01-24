from fastapi import APIRouter, Depends, Path

from market.dataclasses import SignPrice
from market.objects import PERMIT_FOR_ADMIN
from market.schemas import CreatingProduct, Product
from market.services import ProductService

router = APIRouter(tags=['Products'])


@router.get(
    '/products/',
    status_code=200,
    description='Get the product',
)
async def get_products(
        name: str | None = None,
        price: SignPrice = Depends(),
        category_id: int | None = None,
        service: ProductService = Depends()
) -> list[Product]:
    return await service.retrieve_list(name=name, price=price, category_id=category_id)


@router.get(
    '/products/{id}/',
    status_code=200,
    description='Get the products',
)
async def get_product(_id: int = Path(alias='id'), service: ProductService = Depends()) -> Product:
    return await service.retrieve_by_id(_id)


@router.post(
    '/products/',
    status_code=201,
    description='Create a new product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def post_product(product: CreatingProduct, service: ProductService = Depends()) -> None:
    return await service.create(product)


@router.put(
    '/products/{id}/',
    status_code=202,
    description='Update the product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_product(
        data: dict, _id: int = Path(alias='id'), service: ProductService = Depends()
) -> None:
    return await service.update(data, _id)


@router.delete(
    '/products/{id}/',
    status_code=202,
    description='Delete the product',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_product(_id: int = Path(alias='id'), service: ProductService = Depends()) -> None:
    return await service.delete(_id)
