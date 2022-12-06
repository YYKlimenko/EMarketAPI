from sqlalchemy import create_engine

from market.configs import PostgresConfig
from market.models import (  # noqa: F401
    CategoryModel, ProductModel, UserModel, OrderModel,
    ProductOrderLink, ImageModel, TableModel
)


if __name__ == '__main__':
    engine = create_engine(f'postgresql+psycopg2://{PostgresConfig.URL_DB}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
