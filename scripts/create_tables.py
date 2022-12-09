from sqlalchemy import create_engine

from market.configs import PostgresConfig
from market.models import (  # noqa: F401
    CategoryModel, ProductModel, UserModel, OrderModel,
    ProductOrderLink, ImageModel, TableModel
)

def create_tables():
    engine = create_engine(f'postgresql+psycopg2://{PostgresConfig.get_url_db()}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_tables()
