import logging

from fastapi import APIRouter, Body, Depends

from auth.service import AuthorizationService


logger = logging.getLogger(__name__)


router = APIRouter(tags=['Authorization & Authentication'])


@router.post('/authentication/', status_code=202, description='Authentication user')
async def authorize_user(
        login: str = Body(...),
        password: str = Body(...),
        service=Depends(AuthorizationService),
) -> dict[str, str]:
    print("===================")
    logger.info('=============================')
    return await service.authorize(login, password)
