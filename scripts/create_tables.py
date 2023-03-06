from sqlalchemy import create_engine

from common.configs import AbstractSQLConfig
from market.models import (CategoryModel, ImageModel, OrderModel, TableModel,  # noqa: F401
                           ProductModel, ProductOrderLink, UserModel)


def create_tables(config: AbstractSQLConfig):
    engine = create_engine(f'postgresql+psycopg2://{config.get_url_db()}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
