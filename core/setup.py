from fastapi import APIRouter, Depends

from core.permissions.permissions import permit_by_secret_key
from market.configs import PostgresConfig
from scripts.create_superusers import create_superuser
from scripts.create_tables import create_tables

router = APIRouter(tags=['Setup'])


@router.post(
    '/create_tables/',
    status_code=200,
    description='Create tables in DB',
    dependencies=[Depends(permit_by_secret_key)]
)
def create_data(secret_key: str) -> None:
    return create_tables()


@router.post(
    '/create_superusers/',
    status_code=200,
    description='Create super user in DB',
    dependencies=[Depends(permit_by_secret_key)]
)
async def post_superuser(secret_key: str, config: PostgresConfig = Depends()) -> None:
    return await create_superuser(config)
