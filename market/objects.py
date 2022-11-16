from fastapi import Depends

from core.permissions.permissions import permit_for_owner, permit_for_admin
from core.repositories import SQLAsyncRepository
from market.models import CategoryModel, ImageModel, OrderModel, ProductModel, UserModel
from market.permissions import permit_post_order_for_owner, permit_for_user, \
    permit_get_order_for_owner
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

PERMIT_GET_ORDER_FOR_OWNER = Depends(permit_get_order_for_owner)
PERMIT_POST_ORDER_FOR_OWNER = Depends(permit_post_order_for_owner)
PERMIT_FOR_USER = Depends(permit_for_user)
PERMIT_FOR_OWNER = Depends(permit_for_owner)
PERMIT_FOR_ADMIN = Depends(permit_for_admin)
