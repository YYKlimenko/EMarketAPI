from .service import Authenticator, Authorizator
from .settings import SECRET_KEY, UserService, repository

auth_service = UserService(repository)
authorizator = Authorizator(SECRET_KEY, auth_service)
authenticator = Authenticator(SECRET_KEY)
