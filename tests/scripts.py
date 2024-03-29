from datetime import datetime

from bcrypt import gensalt, hashpw
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from market.models import (CategoryModel, OrderModel, ProductModel, TableModel,
                           UserModel)


def create_test_data(engine):

    with Session(engine) as session:
        instances = [
            UserModel(
                username='admin',
                number='88888888888',
                password=hashpw('admin'.encode(), gensalt()).decode(),
                date_registration=datetime.utcnow(),
                is_admin=True),
            UserModel(
                username='user',
                number='99999999999',
                password=hashpw('user'.encode(), gensalt()).decode(),
                date_registration=datetime.utcnow(),
                is_admin=False
            ),
            CategoryModel(
                name='Test category 1'
            ),
            CategoryModel(
                name='Test category 2'
            ),
            product := ProductModel(
                name='Product 1',
                description='Description of Product 1',
                constitution='Constitution of Product 1',
                price=99.99,
                category_id=1
            ),
            OrderModel(
                user_id=1,
                products=[product]
            )
        ]
        session.add_all(instances)
        session.commit()


def create_tables(config):
    engine = create_engine(f'postgresql+psycopg2://{config().get_url_db()}')
    TableModel.metadata.drop_all(engine)
    TableModel.metadata.create_all(engine)
    create_test_data(engine)
