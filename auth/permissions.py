import os
from typing import Any

from fastapi import Depends, HTTPException

from auth.service import Authenticator
from auth.configs import AuthConfig


def permit_for_admin(auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)) -> bool:
    if not auth_data['is_admin']:
        raise HTTPException(401, 'You\'re don\'t have permission')
    return True


def permit_for_owner(
        user_id: int | None = None,
        auth_data: dict[str, Any] = Depends(Authenticator.handle_auth)
) -> True:
    if auth_data['is_admin'] or user_id == auth_data['sub']:
        return True
    else:
        raise HTTPException(401, 'You\'re don\'t have permission')


def permit_by_secret_key(
        secret_key: str,
        config: AuthConfig = Depends()
) -> True:
    if secret_key == config.SECRET_KEY:
        return True
    else:
        raise HTTPException(401, 'You\'re don\'t have permission')
