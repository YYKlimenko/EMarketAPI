from fastapi import APIRouter, Depends


from auth.repositories import SQLAuthorizationRepository
from auth.services.service import AuthorizationService
from auth.settings import SECRET_KEY, USER_MODEL
router = APIRouter(tags=['Authorization & Authentication'])

repository = SQLAuthorizationRepository(USER_MODEL)
auth_service = AuthorizationService(SECRET_KEY, repository)


@router.post('/authorization/', status_code=202, description='Authorize user')
def authorize_user(response: dict[str, str] = Depends(auth_service.authorize)) -> dict[str, str]:
    return response
