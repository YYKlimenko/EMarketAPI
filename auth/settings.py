from core.settings import get_async_session, SECRET_KEY, repository
from .models import CreatingUser, User
from market.services import UserService

JWT_KEY = SECRET_KEY
