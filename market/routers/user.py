from fastapi import APIRouter, Depends

from auth.objects import authenticator
from auth.models import RetrievingUser
from core.settings import repository
from market.services import UserService


router = APIRouter(tags=['Users'])
service = UserService(repository)


@router.get('/users/')
async def get_users(response: list[RetrievingUser] = Depends(service.retrieve_list)) -> list[RetrievingUser]:
    return response


@router.get('/users/{id}')
async def get_user(response: RetrievingUser = Depends(service.retrieve_by_id)) -> RetrievingUser:
    return response


@router.delete('/users/{id}')
async def delete_user(response: None = Depends(service.delete)) -> None:
    return response


@router.post('/users/registration/', status_code=201, description='Create new user')
def registrate_user(response: None = Depends(service.registrate)) -> None:
    return response


@router.patch('/users/{user_id}/', status_code=202, description='Change user\'s data')
def change_user_data(response: dict[str, str] = Depends(service.change_data)) -> dict[str, str]:
    return response