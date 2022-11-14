from typing import Any

from fastapi import Depends, HTTPException

from auth.objects import authenticator
from core.settings import SUPERUSERS


def permit_for_admin(auth_data: dict[str, Any] = Depends(authenticator.handle_auth)) -> bool:
    if auth_data['sub'] not in SUPERUSERS:
        raise HTTPException(401, 'You\'re don\'t have permission')
    return True


def permit_for_owner(
        user_id: int,  auth_data: dict[str, Any] = Depends(authenticator.handle_auth)
) -> True:
    if permit_for_admin(auth_data) or user_id == auth_data['sub']:
        return True
    raise HTTPException(401, 'You\'re don\'t have permission')


PERMIT_FOR_OWNER = Depends(permit_for_owner)
PERMIT_FOR_ADMIN = Depends(permit_for_admin)
