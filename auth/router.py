from fastapi import APIRouter, Depends


from market.models import UserModel
from auth.repositories import SQLAuthorizationRepository
from auth.service import AuthorizationService
from auth.settings import SECRET_KEY
router = APIRouter(tags=['Authorization & Authentication'])

repository = SQLAuthorizationRepository(UserModel)
auth_service = AuthorizationService(SECRET_KEY, repository)


@router.post('/authorization/', status_code=202, description='Authorize user')
def authorize_user(response: dict[str, str] = Depends(auth_service.authorize)) -> dict[str, str]:
    return response
