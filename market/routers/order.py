from fastapi import APIRouter, Depends

from auth.objects import authenticator
from core.settings import repository
from market.models import Order
from market.services import OrderService

router = APIRouter(tags=['Orders'])
service = OrderService(repository)


@router.get('/orders/')
async def get_orders(response: list[Order] = Depends(service.retrieve_list)) -> list[Order]:
    return response


@router.get('/order/{id}')
async def get_order(response: Order = Depends(service.retrieve_by_id)) -> Order:
    return response


@router.post('/orders/')
async def post_order(response: None = Depends(service.create)) -> None:
    return response


@router.put('/orders/{id}')
async def put_order(response: None = Depends(service.update)) -> None:
    return response


@router.delete('/orders/{id}')
async def delete_order(response: None = Depends(service.delete)) -> None:
    return response
