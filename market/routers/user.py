from fastapi import APIRouter, Depends

from market.schemas import User
from market.objects import user_service as service, PERMIT_FOR_ADMIN, PERMIT_FOR_USER

router = APIRouter(tags=['Users'])


@router.get(
    '/users/',
    status_code=200,
    description='Get a list of users',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def get_users(response: list[User] = Depends(service.retrieve_list)):
    return response


@router.get(
    '/users/{id}',
    status_code=200,
    description='Get the user',
    dependencies=[PERMIT_FOR_USER]
)
async def get_user(response: User = Depends(service.retrieve_by_id)):
    return response


@router.delete(
    '/users/{id}',
    status_code=202,
    description='Delete the user',
    dependencies=[PERMIT_FOR_USER]
)
async def delete_user(response: None = Depends(service.delete)):
    return response


@router.post('/users/registration/', status_code=201, description='Create the new user')
def registrate_user(response: None = Depends(service.registrate)):
    return response


@router.put(
    '/users/{id}',
    status_code=202,
    description='Change user data',
    dependencies=[PERMIT_FOR_USER]
)
def change_user_data(response: None = Depends(service.update)) -> None:
    return response
