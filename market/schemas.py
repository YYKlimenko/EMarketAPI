import string
from datetime import datetime

from pydantic import BaseModel, Field, condecimal, validator


class ID(BaseModel):
    """
    Pydantic schema including id-field for inheritance
    """
    id: int


class CreatingProduct(BaseModel):
    """
    Pydantic schema for create Product instance in DB
    """
    name: str = Field(max_length=60)
    description: str = Field(max_length=1000)
    constitution: str = Field(max_length=1000)
    price: condecimal(max_digits=10, decimal_places=3)
    category_id: int


class Product(CreatingProduct, ID):
    """
    Pydantic schema for retrieve Product instance from DB
    """
    pass


class CreatingCategory(BaseModel):
    """
    Pydantic schema for create Category instance in DB
    """
    name: str = Field(max_length=60)


class Category(CreatingCategory, ID):
    """
    Pydantic schema for retrieve Category instance from DB
    """
    pass


class CreatingImage(BaseModel):
    """
    Pydantic schema for create Image instance from DB
    """
    url: str
    product_id: int


class Image(CreatingImage, ID):
    """
    Pydantic schema for retrieve Image instance from DB
    """
    pass


class BaseUser(BaseModel):
    username: str = Field(max_length=30, default='username')
    number: str = Field(max_length=12, default='89050965588')


class CreatingUser(BaseUser):
    """
    Pydantic schema for create User instance from DB
    """
    password: str = Field(max_length=256, default='password')
    password2: str = Field(max_length=256, default='password')

    @validator('password2')
    def match_passwords(cls, password2: str, values: dict[str, str]) -> str:
        password = values.get('password')
        if password and password2 != password:
            raise ValueError('Passwords don\'t match')
        else:
            return password2

    @validator('number')
    def check_number(cls, number: str, values: dict[str, str]) -> str:
        begin = 1 if number[0] == '+' else 0
        length = 12 if number[0] == '+' else 11

        if len(number) == length:
            for n in number[begin:]:
                if n not in string.digits:
                    break
            else:
                return number
        raise ValueError('Telephone number is not correct')


class User(BaseUser, ID):
    """
    Pydantic schema for retrieve User instance from DB
    """
    date_registration: datetime = datetime.utcnow()
    is_admin: bool = False


class BaseOrder(BaseModel):
    user_id: int


class CreatingOrder(BaseOrder):
    """
    Pydantic schema for create Order instance from DB
    """
    products: list[int]

    @validator('products')
    def check_list(cls, products: list[int], values: dict[str, str]) -> list[int]:
        if len(products):
            return products
        else:
            raise ValueError('The product list can\'t to be empty')


class Order(BaseOrder, ID):
    """
      Pydantic schema for retrieve Order instance from DB
      """
    products: list[Product]
