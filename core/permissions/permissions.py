from typing import Any

from fastapi import Depends, HTTPException

from auth.objects import authenticator
from settings import SUPERUSERS


def is_admin(user_id):
    return True if user_id in SUPERUSERS else False


def permit_for_admin(auth_data: dict[str, Any] = Depends(authenticator.handle_auth)) -> bool:
    if not is_admin(auth_data['sub']):
        raise HTTPException(401, 'You\'re don\'t have permission')
    return True


def permit_for_owner(
        user_id: int | None = None,
        auth_data: dict[str, Any] = Depends(authenticator.handle_auth)
) -> True:
    if is_admin(auth_data['sub']) or user_id == auth_data['sub']:
        return True
    else:
        raise HTTPException(401, 'You\'re don\'t have permission')
