from fastapi import APIRouter, Depends

from auth.objects import auth_service
router = APIRouter(tags=['Authorization & Authentication'])


@router.post('/authorization/', status_code=202, description='Authorize user')
def authorize_user(response: dict[str, str] = Depends(auth_service.authorize)) -> dict[str, str]:
    return response
