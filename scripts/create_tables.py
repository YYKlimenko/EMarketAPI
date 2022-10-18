from sqlmodel import SQLModel, create_engine

from auth.models import *
from core.settings import URL_DB
from market.models import *


if __name__ == '__main__':
    engine = create_engine(f'postgresql+psycopg2://{URL_DB}')
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
