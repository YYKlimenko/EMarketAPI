from auth.permissions import permit_by_secret_key
from fastapi import APIRouter, Depends
from market.configs import PostgresConfig, PostgresConfigDev
from scripts.create_superusers import create_superuser
from scripts.create_tables import create_tables


from fastapi import FastAPI


router = APIRouter(tags=['Setup'])


@router.post(
    '/create_tables/',
    status_code=200,
    description='Create tables in DB',
    dependencies=[Depends(permit_by_secret_key)]
)
def create_data(secret_key: str, config: PostgresConfig = Depends()) -> None:
    return create_tables(config)


@router.post(
    '/create_superusers/',
    status_code=200,
    description='Create super user in DB',
    dependencies=[Depends(permit_by_secret_key)]
)
async def post_superuser(secret_key: str, config: PostgresConfig = Depends()) -> None:
    return await create_superuser(config)

setup = FastAPI(debug=True)
setup.include_router(router)


@setup.on_event("startup")
async def startup_event():
    if setup.debug:
        setup.dependency_overrides[PostgresConfig] = PostgresConfigDev
