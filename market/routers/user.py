from fastapi import APIRouter, Depends

from core.repositories import SQLAsyncRepository
from market.models import UserModel
from market.schemas import User, CreatingUser
from market.services import UserService

router = APIRouter(tags=['Users'])
repository = SQLAsyncRepository(UserModel)
service = UserService(repository, CreatingUser, User, ['number', 'username'])


@router.get('/users/', status_code=200, description='Get a list of users')
async def get_users(
        response: list[User] = Depends(service.retrieve_list)
) -> list[User]:
    return response


@router.get('/users/{id}', status_code=200, description='Get the user')
async def get_user(response: User = Depends(service.retrieve_by_id)) -> User:
    return response


@router.delete('/users/{id}', status_code=202, description='Delete the user')
async def delete_user(response: None = Depends(service.delete)) -> None:
    return response


@router.post('/users/registration/', status_code=201, description='Create the new user')
def registrate_user(response: None = Depends(service.registrate)) -> None:
    return response


@router.put('/users/{id}', status_code=202, description='Change user data')
def change_user_data(response: None = Depends(service.update)) -> None:
    return response
