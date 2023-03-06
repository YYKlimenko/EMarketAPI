import datetime

from bcrypt import gensalt, hashpw

from market.models import UserModel  # noqa: F401


async def create_superuser(config):
    session_maker = config.get_session_maker()
    session = session_maker()
    user = UserModel(
        username='admin',
        number='89006772323',
        password=hashpw('admin'.encode(), gensalt()).decode(),
        date_registration=datetime.datetime.utcnow(),
        is_admin=True
    )
    session.add(user)
    await session.commit()
