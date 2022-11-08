from auth.repositories import SQLAuthorizationRepository
from auth.services.service import AuthorizationService
from auth.settings import SECRET_KEY, USER_MODEL


repository = SQLAuthorizationRepository(USER_MODEL)
auth_service = AuthorizationService(SECRET_KEY, repository)
