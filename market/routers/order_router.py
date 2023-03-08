from typing import Any

from fastapi import APIRouter, Depends

from common.functions import get_fields
from common.permissions import permit_for_owner
from market.schemas import RetrievingOrderSchema, CreatingOrderSchema
from market.services import OrderService
from market.permissions import permit_get_order_for_owner, permit_post_order_for_owner

order_router = APIRouter(prefix='/orders', tags=['Orders'])


@order_router.get(
    '/',
    status_code=200,
    description='Get a list of the orders',
    response_model=list[RetrievingOrderSchema],
    dependencies=[Depends(permit_for_owner)],
)
async def get_orders(user_id: int | None = None, service: OrderService = Depends()) -> list[dict[str, Any]]:
    return await service.retrieve(many=True, **get_fields(user_id=user_id))


@order_router.get(
    '/{order_id}/',
    status_code=200,
    description='Get the order',
    response_model=RetrievingOrderSchema | None,
    dependencies=[Depends(permit_get_order_for_owner)],
)
async def get_order(order_id: int, service: OrderService = Depends()) -> dict[str, Any]:
    return await service.retrieve(id=order_id)


@order_router.post(
    '/',
    status_code=201,
    description='Create the order',
    dependencies=[Depends(permit_post_order_for_owner)],
)
async def post_order(order: CreatingOrderSchema, service: OrderService = Depends()) -> None:
    return await service.create(order.dict())


@order_router.delete(
    '/{order_id}/',
    status_code=202,
    description='Delete the order',
    dependencies=[Depends(permit_post_order_for_owner)],
)
async def delete_order(order_id: int, service: OrderService = Depends()) -> None:
    return await service.delete(order_id)
