from core.repositories import SQLAsyncRepository
from market.schemas import User, CreatingUser
from market.services import UserService
from .service import Authenticator, Authorizator
from .settings import SECRET_KEY
from market.models import UserModel

repository = SQLAsyncRepository(UserModel)
auth_service = UserService(repository, User, CreatingUser)
authorizator = Authorizator(SECRET_KEY, auth_service)
authenticator = Authenticator(SECRET_KEY)
