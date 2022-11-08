from core.settings import db, SECRET_KEY, USER_MODEL
from core.services.services import Service  # noqa: F401

JWT_KEY = SECRET_KEY
DB_CONNECTOR = db
USER_MODEL = USER_MODEL
