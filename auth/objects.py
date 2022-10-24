from .service import Authenticator, Authorizator
from .settings import SECRET_KEY, UserService, repository_class

auth_service = UserService(repository_class)
authorizator = Authorizator(SECRET_KEY, auth_service)
authenticator = Authenticator(SECRET_KEY)
