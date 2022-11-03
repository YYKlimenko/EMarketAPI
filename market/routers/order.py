from fastapi import APIRouter, Depends

from core.repositories import SQLAsyncRepository
from market.models import OrderModel
from market.schemas import Order, CreatingOrder
from market.services import OrderService

router = APIRouter(tags=['Orders'])
repository = SQLAsyncRepository(OrderModel)
service = OrderService(repository, Order, CreatingOrder)


# @router.get('/orders/', status_code=200, description='Get a list of orders')
# async def get_orders(response: list[Order] = Depends(service.retrieve_list)) -> list:
#     return response


@router.get('/order/{id}', status_code=200, description='Get the order')
async def get_order(response: Order = Depends(service.retrieve_by_id)) -> Order:
    return response


@router.post('/orders/', status_code=201, description='Create the order')
async def post_order(response: None = Depends(service.create)) -> None:
    return response


@router.put('/orders/{id}', status_code=202, description='Update the order')
async def put_order(response: None = Depends(service.update)) -> None:
    return response


@router.delete('/orders/{id}', status_code=202, description='Delete the order')
async def delete_order(response: None = Depends(service.delete)) -> None:
    return response
