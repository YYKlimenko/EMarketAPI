from fastapi import APIRouter, Depends

from auth.objects import authorizator

router = APIRouter(tags=['Authorization & Authentication'])


@router.post('/authorization/', status_code=202, description='Authorize user')
def authorize_user(response: dict[str, str] = Depends(authorizator.authorize)) -> dict[str, str]:
    return response
