from sqlalchemy import Boolean, Column, DateTime, DECIMAL, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base


TableModel = declarative_base()

ProductOrderLink = Table(
    'product_order_link',
    TableModel.metadata,
    Column('order_id', ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
)


class ProductModel(TableModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String(1000), nullable=False)
    constitution = Column(String(1000), nullable=False)
    price = Column(DECIMAL(), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('CategoryModel', back_populates='products')
    orders = relationship('OrderModel', secondary=ProductOrderLink, back_populates='products')
    images = relationship('ImageModel', back_populates='product', cascade='all, delete-orphan')


class CategoryModel(TableModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)

    products = relationship('ProductModel', back_populates='category', cascade='all, delete-orphan')


class ImageModel(TableModel):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    url = Column(String(60), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('ProductModel', back_populates='images')


class UserModel(TableModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False, index=True)
    number = Column(String(12), unique=True, nullable=False)
    password = Column(String(256))
    date_registration = Column(DateTime)
    is_admin = Column(Boolean)

    orders = relationship('OrderModel', back_populates='user', cascade='all, delete-orphan')


class OrderModel(TableModel):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('UserModel', back_populates='orders')
    products = relationship('ProductModel', secondary=ProductOrderLink, back_populates='orders')
