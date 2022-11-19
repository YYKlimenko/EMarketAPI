import asyncio
import datetime

from bcrypt import hashpw, gensalt

from core.settings import session_maker
from market.models import TableModel, UserModel  # noqa: F401


async def create_superuser(session):
    session = session()
    user = UserModel(
        username='admin',
        number='89006772323',
        password=hashpw('admin'.encode(), gensalt()).decode(),
        date_registration=datetime.datetime.utcnow(),
        is_admin=True
    )
    session.add(user)
    await session.commit()


if __name__ == '__main__':
    asyncio.run(create_superuser(session_maker))
