from fastapi import APIRouter, Depends, Path

from market.schemas import CreatingUser, User
from market.objects import PERMIT_FOR_ADMIN, PERMIT_FOR_USER
from market.services import UserService

router = APIRouter(tags=['Users'])


@router.get(
    '/users/',
    status_code=200,
    description='Get a list of users',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def get_users(
        username: str | None = None, number: str | None = None, service: UserService = Depends()
) -> list[User]:
    return await service.retrieve_list(username=username, number=number)


@router.get(
    '/users/{id}/',
    status_code=200,
    description='Get the user',
    dependencies=[PERMIT_FOR_USER]
)
async def get_user(_id: int = Path(alias='id'), service: UserService = Depends()) -> User:
    return await service.retrieve_by_id(_id)


@router.delete(
    '/users/{id}/',
    status_code=202,
    description='Delete the user',
    dependencies=[PERMIT_FOR_USER]
)
async def delete_user(_id: int = Path(alias='id'), service: UserService = Depends()) -> None:
    return await service.delete(_id)


@router.post('/users/registration/', status_code=201, description='Create the new user')
async def registrate_user(user: CreatingUser, service: UserService = Depends()) -> None:
    return await service.registrate(user)


@router.put(
    '/users/{id}/',
    status_code=202,
    description='Change user data',
    dependencies=[PERMIT_FOR_USER]
)
async def change_user_data(
        data: dict, _id: int = Path(alias='id'), service: UserService = Depends()
) -> None:
    return await service.update(data, _id)
