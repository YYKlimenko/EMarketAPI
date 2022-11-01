from fastapi import APIRouter, Depends

from auth.objects import authenticator
from auth.models import RetrievingUser, User, CreatingUser
from core.settings import repository
from market.services import UserService

router = APIRouter(tags=['Users'])
service = UserService(repository, User, CreatingUser, RetrievingUser, ['number', 'username'])


@router.get('/users/', status_code=200, description='Get a list of users')
async def get_users(
        response: list[RetrievingUser] = Depends(service.retrieve_list)
) -> list[RetrievingUser]:
    return response


@router.get('/users/{id}', status_code=200, description='Get the user')
async def get_user(response: RetrievingUser = Depends(service.retrieve_by_id)) -> RetrievingUser:
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
