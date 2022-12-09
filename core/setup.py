from fastapi import APIRouter, Depends

from market.configs import PostgresConfig
from scripts.create_superusers import create_superuser
from scripts.create_tables import create_tables

router = APIRouter(tags=['Setup'])


@router.post(
    '/create_tables/',
    status_code=200,
    description='Create tables in DB',
)
def create_data() -> None:
    return create_tables()


@router.post(
    '/create_superusers/',
    status_code=200,
    description='Create super user in DB',
)
async def post_superuser(config: PostgresConfig = Depends()) -> None:
    return await create_superuser(config)
