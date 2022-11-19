from fastapi import APIRouter, Depends, Body

from auth.service import AuthorizationService
router = APIRouter(tags=['Authorization & Authentication'])


@router.post('/authorization/', status_code=202, description='Authorize user')
async def authorize_user(
        login: str = Body(...),
        password: str = Body(...),
        service=Depends(AuthorizationService)
) -> dict[str, str]:
    return await service.authorize(login, password)
