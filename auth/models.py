from datetime import datetime
from string import digits

from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship


class IDUser(SQLModel):
    id: int = Field(primary_key=True)


class BaseUser(SQLModel):
    username: str = Field(
        max_length=30, index=True, sa_column_kwargs={'unique': True}
    )
    number: str = Field(max_length=12)

    @validator('number')
    def check_number(cls, number: str, values: dict[str, str]) -> str:
        begin = 1 if number[0] == '+' else 0
        length = 12 if number[0] == '+' else 11

        if len(number) == length:
            for n in number[begin:]:
                if n not in digits:
                    break
            else:
                return number
        raise ValueError('Telephone number is not correct')


class CreatingUser(BaseUser, SQLModel):
    password: str = Field(max_length=256)
    password2: str = Field(max_length=256)

    @validator('password2')
    def match_passwords(cls, password2: str, values: dict[str, str]) -> str:
        password = values.get('password')
        if password and password2 != password:
            raise ValueError('Passwords don\'t match')
        else:
            return password2


class RetrievingUser(BaseUser, IDUser):
    date_registration: datetime = datetime.utcnow()
    is_admin: bool = False


class User(RetrievingUser, table=True):
    __tablename__ = 'Users'

    hashed_password: str = Field(max_length=256)

    orders: list['Order'] = Relationship(back_populates="user")
