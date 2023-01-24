from fastapi import APIRouter, Body, Depends

from auth.service import AuthorizationService

router = APIRouter(tags=['Authorization & Authentication'])


@router.post('/authentication/', status_code=202, description='Authentication user')
async def authorize_user(
        login: str = Body(...),
        password: str = Body(...),
        service=Depends(AuthorizationService)
) -> dict[str, str]:
    return await service.authorize(login, password)
