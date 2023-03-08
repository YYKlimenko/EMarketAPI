from typing import Any

from fastapi import Depends, HTTPException, Path

from auth.service import Authenticator
from common.permissions import permit_for_owner

from market.repositories import OrderSQLRepository
from market.schemas import CreatingOrderSchema


async def permit_get_order_for_owner(
        order_id: int | None,
        repository: OrderSQLRepository = Depends(),
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth),
):
    order = await repository.retrieve(filter_fields={'id': order_id})
    if order:
        return permit_for_owner(order[0]['user_id'], auth_data)


def permit_post_order_for_owner(
        order: CreatingOrderSchema,
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
) -> bool:
    if auth_data['is_admin'] or order.user_id == auth_data['sub']:
        return True
    raise HTTPException(401, 'You\'re don\'t have permission')


def permit_for_user(
        user_id: int = Path(alias='id'),
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
):
    return permit_for_owner(user_id, auth_data)
