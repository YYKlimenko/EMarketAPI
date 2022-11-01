from auth.models import User, CreatingUser, RetrievingUser
from market.services import UserService
from .service import Authenticator, Authorizator
from .settings import SECRET_KEY, repository


auth_service = UserService(repository, User, CreatingUser, RetrievingUser)
authorizator = Authorizator(SECRET_KEY, auth_service)
authenticator = Authenticator(SECRET_KEY)
