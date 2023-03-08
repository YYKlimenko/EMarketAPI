from typing import Any

from fastapi import APIRouter, Depends, Path

from common.functions import get_fields
from common.permissions import permit_for_admin, permit_for_owner
from market.permissions import permit_for_user
# from market.objects import PERMIT_FOR_ADMIN, PERMIT_FOR_USER
from market.schemas import CreatingUserSchema, RetrievingUserSchema, UpdatingUserSchema
from market.services import UserService

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get(
    '/',
    status_code=200,
    description='Get a list of users',
    dependencies=[Depends(permit_for_admin)],
    response_model=list[RetrievingUserSchema]
)
async def get_users(is_admin:  bool | None = None, service: UserService = Depends()) -> list[dict[str, Any]]:
    """Retrieve list of users."""
    return await service.retrieve(many=True, **get_fields(is_admin=is_admin))


@user_router.get(
    '/{user_id}/',
    status_code=200,
    description='Get the user',
    dependencies=[Depends(permit_for_owner)],
    response_model=RetrievingUserSchema | None
)
async def get_user(user_id: int, service: UserService = Depends()) -> dict[str, Any] | None:
    return await service.retrieve(id=user_id)


@user_router.delete(
    '/{user_id}/',
    status_code=202,
    description='Delete the user',
    dependencies=[Depends(permit_for_owner)],
)
async def delete_user(user_id: int, service: UserService = Depends()) -> None:
    return await service.delete(user_id)


@user_router.post('/registration/', status_code=201, description='Create the new user')
async def registrate_user(user: CreatingUserSchema, service: UserService = Depends()) -> None:
    return await service.create(user.dict(exclude={'password2'}))


@user_router.put(
    '/{user_id}/',
    status_code=202,
    description='Change user data',
    dependencies=[Depends(permit_for_owner)],
)
async def change_user_data(data: UpdatingUserSchema, user_id: int, service: UserService = Depends()) -> None:
    return await service.update(user_id, get_fields(**data.dict()))
