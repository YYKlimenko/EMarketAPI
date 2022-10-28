from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship


class ID(SQLModel):
    id: int = Field(primary_key=True)


class CreatingProductCategory(SQLModel):
    name: str = Field(max_length=60)


class ProductCategory(CreatingProductCategory, ID, table=True):
    __tablename__ = 'Categories'


class ProductOrderLink(SQLModel, table=True):
    product_id: int | None = Field(
        default=None, foreign_key="Products.id", primary_key=True
    )
    order_id: int | None = Field(
        default=None, foreign_key="Orders.id", primary_key=True
    )


class CreatingProduct(SQLModel):
    name: str = Field(max_length=60)
    description: str = Field(max_length=1000)
    constitution: str = Field(max_length=1000)
    price: condecimal(max_digits=10, decimal_places=3)

    category_id: int = Field(foreign_key='Categories.id')
    category: ProductCategory = Relationship(back_populates='products')


class Product(CreatingProduct, ID, table=True):
    __tablename__ = 'Products'

    orders: list['Order'] = Relationship(back_populates="products",
                                         link_model=ProductOrderLink)
    images: list['Image'] = Relationship(back_populates="product")


class CreatingImage(SQLModel):
    url: str

    product_id: int = Field(foreign_key='Products.id')
    product: Product = Relationship(back_populates='images')


class Image(CreatingImage, ID, table=True):
    __tablename__ = 'Images'
    product_id: int = Field(foreign_key='Products.id')
    product: Product = Relationship(back_populates='images')


class BaseOrder(SQLModel):
    user_id: int = Field(foreign_key='Users.id')


class CreatingOrder(BaseOrder, SQLModel):
    products_id: list[int]


class Order(BaseOrder, ID, table=True):
    __tablename__ = 'Orders'

    user: 'User' = Relationship(back_populates='orders')
    products: list[Product] = Relationship(back_populates="orders", link_model=ProductOrderLink)
