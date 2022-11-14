from core.repositories import SQLAsyncRepository
from market.models import CategoryModel, ImageModel, OrderModel, ProductModel, UserModel
from market.repositories import OrderAsyncPostgresRepository
from market.schemas import (
    CreatingCategory, Category, Image, CreatingProduct, Product, CreatingImage,
    CreatingUser, User
)
from market.services import CategoryService, ImageService, OrderService, ProductService, UserService

category_repository = SQLAsyncRepository(CategoryModel)
category_service = CategoryService(category_repository, CreatingCategory, Category)

image_repository = SQLAsyncRepository(ImageModel)
image_service = ImageService(image_repository, Image, CreatingImage)

order_repository = OrderAsyncPostgresRepository(OrderModel)
order_service = OrderService(order_repository, ['user_id'])

product_repository = SQLAsyncRepository(ProductModel)
product_service = ProductService(product_repository, CreatingProduct, Product)

user_repository = SQLAsyncRepository(UserModel)
user_service = UserService(user_repository, CreatingUser, User, ['number', 'username'])
