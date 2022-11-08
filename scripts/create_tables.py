from sqlalchemy import create_engine

from core.settings import URL_DB
from market.models import (  # noqa: F401
    CategoryModel, ProductModel, UserModel, OrderModel,
    ProductOrderLink, ImageModel, TableModel
)


if __name__ == '__main__':
    engine = create_engine(f'postgresql+psycopg2://{URL_DB}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
