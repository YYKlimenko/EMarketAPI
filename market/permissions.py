from typing import Any

from fastapi import Depends, HTTPException, Path
from pydantic import BaseModel

from auth.service import Authenticator
from core.permissions.permissions import permit_for_owner
from market.repositories import OrderRepository
from market.schemas import CreatingOrder


async def permit_get_order_for_owner(
        repository: OrderRepository = Depends(),
        order_id: int | None = Path(alias='id'),
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
):

    class user_id(BaseModel):
        user_id: int

    order = await repository.retrieve(data=user_id, id=(order_id, '=='))
    if order:
        return permit_for_owner(order.user_id, auth_data)


def permit_post_order_for_owner(
        instance: CreatingOrder,
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
) -> bool:
    if auth_data['is_admin'] or instance.user_id == auth_data['sub']:
        return True
    raise HTTPException(401, 'You\'re don\'t have permission')


def permit_for_user(
        user_id: int = Path(alias='id'),
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
):
    return permit_for_owner(user_id, auth_data)
