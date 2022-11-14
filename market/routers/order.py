from fastapi import APIRouter, Depends

from core.permissions.permissions import PERMIT_FOR_ADMIN, PERMIT_FOR_OWNER
from market.schemas import Order
from market.objects import order_service as service


router = APIRouter(tags=['Orders'])


@router.get(
    '/orders/',
    status_code=200,
    description='Get a list of orders',
    dependencies=[PERMIT_FOR_OWNER]
)
async def get_orders(response: list[Order] = Depends(service.retrieve_list)):
    return response


@router.get(
    '/order/{id}',
    status_code=200,
    description='Get the order',
    dependencies=[PERMIT_FOR_OWNER]
)
async def get_order(response: Order = Depends(service.retrieve_by_id)) -> Order:
    return response


@router.post(
    '/orders/',
    status_code=201,
    description='Create the order',
    dependencies=[PERMIT_FOR_OWNER]
)
async def post_order(response: None = Depends(service.create)) -> None:
    return response


@router.put(
    '/orders/{id}',
    status_code=202,
    description='Update the order',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_order(response: None = Depends(service.update)) -> None:
    return response


@router.delete(
    '/orders/{id}',
    status_code=202,
    description='Delete the order',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_order(response: None = Depends(service.delete)) -> None:
    return response
