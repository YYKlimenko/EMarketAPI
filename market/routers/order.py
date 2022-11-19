from fastapi import APIRouter, Depends, Path

from market.schemas import Order, CreatingOrder
from market.objects import (
    PERMIT_FOR_OWNER, PERMIT_POST_ORDER_FOR_OWNER, PERMIT_FOR_ADMIN, PERMIT_GET_ORDER_FOR_OWNER
)
from market.services import OrderService

router = APIRouter(tags=['Orders'])


@router.get(
    '/orders/',
    status_code=200,
    description='Get a list of orders',
    dependencies=[PERMIT_FOR_OWNER]
)
async def get_orders(service=Depends(OrderService)):
    return await service.retrieve_list()


@router.get(
    '/order/{id}',
    status_code=200,
    description='Get the order',
    dependencies=[PERMIT_GET_ORDER_FOR_OWNER]
)
async def get_order(_id: int, service=Depends(OrderService)) -> Order:
    return await service.retrieve_by_id(_id)


@router.post(
    '/orders/',
    status_code=201,
    description='Create the order',
    dependencies=[PERMIT_POST_ORDER_FOR_OWNER]
)
async def post_order(instance: CreatingOrder, service=Depends(OrderService)) -> None:
    return await service.create(instance)


@router.put(
    '/orders/{id}',
    status_code=202,
    description='Update the order',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def put_order(data: dict, _id: int, service=Depends(OrderService)) -> None:
    return await service.put(data, _id)


@router.delete(
    '/orders/{id}',
    status_code=202,
    description='Delete the order',
    dependencies=[PERMIT_GET_ORDER_FOR_OWNER]
)
async def delete_order(_id: int = Path(alias="id"), service=Depends(OrderService)) -> None:
    return await service.delete(_id)
